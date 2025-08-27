<template>
  <div>
    <div class="three-wrap" ref="wrapRef">
      <canvas ref="canvasRef" class="three-canvas"></canvas>
    </div>
    <AiAssistant />
  </div>
  
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue'
import * as THREE from 'three'
import AiAssistant from '../../components/AiAssistant.vue'

const wrapRef = ref(null)
const canvasRef = ref(null)

// 资源与链接（将 0.png-7.png 放在 src/assets/img/ 下）
// 使用 webpack 的 require.context 以避免路径解析问题，并兼容 jpg/png
const ctx = require.context('../../assets/img', false, /\.(png|jpe?g)$/)
const imgMap = {}
ctx.keys().forEach(k => { imgMap[k.replace('./','')] = ctx(k) })
const fallbackImg = imgMap['1.png'] || imgMap['Logo.png'] || ''
const imageFiles = Array.from({ length: 8 }, (_, i) => imgMap[`${i}.png`] || imgMap[`${i}.jpg`] || fallbackImg)
const links = [
  'https://example.com/0',
  'https://example.com/1',
  'https://example.com/2',
  'https://example.com/3',
  'https://example.com/4',
  'https://example.com/5',
  'https://example.com/6',
  'https://example.com/7'
]
// 每张图片对应的背景色（可按需要调整为接近图片主色）
const bgColors = ['#f5f7fa']

let scene, camera, renderer, group
let textures = []
let meshes = []
let animId
// 交互拾取
const raycaster = new THREE.Raycaster()
const pointer = new THREE.Vector2()
let hoveredIndex = -1

// 仅在按下时允许旋转
const isDragging = ref(false)

// 圆形裁剪：将图片绘制到圆形 canvas，作为纹理
function toCircleDataURL(src, size = 512) {
  return new Promise((resolve) => {
    const img = new Image()
    img.onload = () => {
      const c = document.createElement('canvas')
      c.width = c.height = size
      const ctx = c.getContext('2d')
      ctx.clearRect(0,0,size,size)
      ctx.save()
      ctx.beginPath()
      ctx.arc(size/2, size/2, size/2, 0, Math.PI*2)
      ctx.closePath()
      ctx.clip()
      // 等比填充
      const ratio = Math.min(size/img.width, size/img.height)
      const w = img.width * ratio
      const h = img.height * ratio
      ctx.drawImage(img, (size-w)/2, (size-h)/2, w, h)
      ctx.restore()
      resolve(c.toDataURL('image/png'))
    }
    img.onerror = () => resolve(null)
    img.src = src
  })
}

// 当前旋转角与目标角
let angle = 0
let targetAngle = 0
// 拖动起点
let startX = 0
let startAngleSnapshot = 0
// 当前"选中"的索引（镜头正前方）
let activeIndex = 0

function lerp(a,b,t){ return a+(b-a)*t }

async function init() {
  scene = new THREE.Scene()

  const w = wrapRef.value.clientWidth
  const h = wrapRef.value.clientHeight
  const fov = 35
  camera = new THREE.PerspectiveCamera(fov, w/h, 0.1, 100)
  // 屏幕上方的中心点：抬高相机位置并俯视轻微
  camera.position.set(0, 1.4, 5.5)
  camera.lookAt(0, 1.4, 0)

  renderer = new THREE.WebGLRenderer({ canvas: canvasRef.value, antialias: true, alpha: true })
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
  renderer.setSize(w, h)
  // 启用软阴影
  renderer.shadowMap.enabled = true
  renderer.shadowMap.type = THREE.PCFSoftShadowMap
  
  // 分组，用于整体旋转
  group = new THREE.Group()
  scene.add(group)
  // 整体上移一点
  group.position.y = 0.3
  
  // 灯光与阴影
  const amb = new THREE.AmbientLight(0xffffff, 2.5)
  scene.add(amb)
  const dirLight = new THREE.DirectionalLight(0xffffff, 0.7)
  // 将光源放在屏幕前方（靠近相机方向），并指向场景中心
  dirLight.position.set(0, 3.8, 5.2)
  dirLight.castShadow = true
  dirLight.shadow.mapSize.set(1024, 1024)
  dirLight.shadow.camera.near = 0.1
  dirLight.shadow.camera.far = 20
  dirLight.shadow.bias = -0.0005
  dirLight.shadow.normalBias = 0.02
  dirLight.target.position.set(0, 1.4, 0)
  scene.add(dirLight)
  scene.add(dirLight.target)
  // 半球光，提升整体亮度与层次
  const hemi = new THREE.HemisphereLight(0xffffff, 0x444444, 0.4)
  scene.add(hemi)
  // 接收阴影的地面（影子接收器）
  const groundGeo = new THREE.CircleGeometry(3.0, 64)
  const groundMat = new THREE.ShadowMaterial({ opacity: 0.18 })
  const ground = new THREE.Mesh(groundGeo, groundMat)
  ground.rotation.x = -Math.PI / 2
  ground.position.set(0, 0.9, 0)
  // 横向拉伸，形成椭圆接收区
  ground.scale.set(1.6, 1, 1)
  ground.receiveShadow = true
  scene.add(ground)
  
  // 预处理圆形纹理
  const circUrls = await Promise.all(imageFiles.map(src => toCircleDataURL(src)))
  const loader = new THREE.TextureLoader()
  textures = circUrls.map(u => loader.load(u || fallbackImg))
  // 水平镜像翻转所有纹理
  textures.forEach(tex => {
    if (!tex) return
    tex.center.set(0.5, 0.5)
    tex.repeat.x = -1
    tex.needsUpdate = true
  })

  const count = textures.length
  const radius = 2.5
  const planeSize = 0.85
  meshes = textures.map((tex, i) => {
    const geo = new THREE.PlaneGeometry(planeSize, planeSize)
    const mat = new THREE.MeshLambertMaterial({ map: tex, transparent: true, side: THREE.DoubleSide, alphaTest: 0.5 })
    const mesh = new THREE.Mesh(geo, mat)
    const theta = (i / count) * Math.PI * 2
    const x = Math.cos(theta) * radius
    const z = Math.sin(theta) * radius
    mesh.position.set(x, 1.4, z)
    mesh.lookAt(0, 1.4, 0)
    mesh.userData = { index: i }
    mesh.castShadow = true
    mesh.receiveShadow = false
    group.add(mesh)
    return mesh
  })

  // 初始背景
  setBgColor(activeIndex)

  // 监听（按下拖动）
  const canvas = canvasRef.value
  canvas.addEventListener('mousedown', onDown)
  canvas.addEventListener('mouseup', onUp)
  canvas.addEventListener('mouseleave', onUp)
  canvas.addEventListener('mousemove', onMouseMove)
  // 触控
  canvas.addEventListener('touchstart', onTouchStart, { passive: true })
  canvas.addEventListener('touchend', onTouchEnd, { passive: true })
  canvas.addEventListener('touchcancel', onTouchEnd, { passive: true })
  canvas.addEventListener('touchmove', onTouchMove, { passive: true })

  canvas.addEventListener('dblclick', onDblClickOpen)
  window.addEventListener('resize', onResize)

  animate()
}

function animate(){
  animId = requestAnimationFrame(animate)
  // 自动缓慢旋转（未拖拽时）
  if (!isDragging.value) {
    targetAngle += 0.0008
  }
  // 平滑插值
  angle = lerp(angle, targetAngle, 0.06)
  group.rotation.y = angle
  // 根据朝向调整可见性与透明度，避免后半区误触
  const camForward = new THREE.Vector3(0,0,-1).applyQuaternion(camera.quaternion)
  meshes.forEach((m, i) => {
    const toMesh = new THREE.Vector3().subVectors(m.position, camera.position).normalize()
    const front = camForward.dot(toMesh) > 0 // 前半区
    const mat = m.material
    if (front) {
      mat.opacity = 1.0
    } else {
      mat.opacity = 0.12
    }
    // 悬停缩放（仅前半区）
    const targetScale = (i === hoveredIndex && front) ? 1.4 : 1.0
    m.scale.x = lerp(m.scale.x, targetScale, 0.2)
    m.scale.y = lerp(m.scale.y, targetScale, 0.2)
  })
  renderer.render(scene, camera)
}

function onDown(e){
  isDragging.value = true
  const ev = e.touches ? e.touches[0] : e
  const rect = canvasRef.value.getBoundingClientRect()
  startX = ev.clientX - rect.left
  startAngleSnapshot = targetAngle
}
function onUp(){ isDragging.value = false }

function onMouseMove(e){
  const rect = canvasRef.value.getBoundingClientRect()
  // 始终更新指针用于悬停检测（不需要按下）
  pointer.x = ((e.clientX - rect.left) / rect.width) * 2 - 1
  pointer.y = -((e.clientY - rect.top) / rect.height) * 2 + 1
  updateHover()
  // 仅在按下拖拽时更新旋转
  if (!isDragging.value) return
  const x = e.clientX - rect.left
  const dx = (x - startX) / rect.width // -1..1 相对位移
  const scale = Math.PI // 灵敏度
  targetAngle = startAngleSnapshot + dx * scale
  updateActiveIndex()
}

function onTouchStart(e){
  isDragging.value = true
  if (!e.touches || !e.touches.length) return
  const t = e.touches[0]
  const rect = canvasRef.value.getBoundingClientRect()
  startX = t.clientX - rect.left
  startAngleSnapshot = targetAngle
}
function onTouchEnd(){ isDragging.value = false }
function onTouchMove(e){
  if (!e.touches || !e.touches.length) return
  const t = e.touches[0]
  const rect = canvasRef.value.getBoundingClientRect()
  // 更新 hover 的指针坐标（移动端仅用于统一逻辑，不会出现 hover 态）
  pointer.x = ((t.clientX - rect.left) / rect.width) * 2 - 1
  pointer.y = -((t.clientY - rect.top) / rect.height) * 2 + 1
  updateHover()
  if (!isDragging.value) return
  const x = t.clientX - rect.left
  const dx = (x - startX) / rect.width
  const scale = Math.PI * 0.8
  targetAngle = startAngleSnapshot + dx * scale
  updateActiveIndex()
}

function updateActiveIndex(){
  const count = meshes.length
  const step = (Math.PI*2)/count
  let rawIndex = Math.round((-angle) / step) % count
  if (rawIndex < 0) rawIndex += count
  if (rawIndex !== activeIndex){
    activeIndex = rawIndex
    setBgColor(activeIndex)
  }
}

function setBgColor(i){
  const wrap = wrapRef.value
  if (!wrap) return
  wrap.style.background = bgColors[i % bgColors.length]
}

function onDblClickOpen(){
  // 仅当前半区才响应
  const m = meshes[activeIndex]
  if (!m) return
  const camForward = new THREE.Vector3(0,0,-1).applyQuaternion(camera.quaternion)
  const front = camForward.dot(new THREE.Vector3().subVectors(m.position, camera.position).normalize()) > 0
  if (!front) return
  const url = links[activeIndex]
  if (url) window.open(url, '_blank')
}

function onResize(){
  if (!renderer || !camera) return
  const w = wrapRef.value.clientWidth
  const h = wrapRef.value.clientHeight
  camera.aspect = w/h
  camera.updateProjectionMatrix()
  renderer.setSize(w, h)
}

onMounted(() => { init() })

onBeforeUnmount(() => {
  cancelAnimationFrame(animId)
  window.removeEventListener('resize', onResize)
  const canvas = canvasRef.value
  if (canvas){
    canvas.removeEventListener('mousedown', onDown)
    canvas.removeEventListener('mouseup', onUp)
    canvas.removeEventListener('mouseleave', onUp)
    canvas.removeEventListener('mousemove', onMouseMove)
    canvas.removeEventListener('touchstart', onTouchStart)
    canvas.removeEventListener('touchend', onTouchEnd)
    canvas.removeEventListener('touchcancel', onTouchEnd)
    canvas.removeEventListener('touchmove', onTouchMove)
    canvas.removeEventListener('dblclick', onDblClickOpen)
  }
  // 释放资源
  textures.forEach(t => t && t.dispose && t.dispose())
  meshes.forEach(m => m.geometry.dispose())
  renderer && renderer.dispose && renderer.dispose()
})

// 悬停检测（仅前半区允许成为 hovered）
function updateHover(){
  if (!renderer || !camera) return
  raycaster.setFromCamera(pointer, camera)
  const intersects = raycaster.intersectObjects(meshes, false)
  let idx = -1
  if (intersects.length){
    const obj = intersects[0].object
    const i = meshes.indexOf(obj)
    if (i >= 0){
      const camForward = new THREE.Vector3(0,0,-1).applyQuaternion(camera.quaternion)
      const front = camForward.dot(new THREE.Vector3().subVectors(obj.position, camera.position).normalize()) > 0
      if (front) idx = i
    }
  }
  hoveredIndex = idx
}
</script>

<style scoped>
.three-wrap { position: relative; width: 100%; height: calc(100vh - 120px); transition: background-color .35s ease; display: flex; align-items: flex-start; justify-content: center; }
.three-canvas { width: 100%; height: 100%; display: block; }
.hint { position: absolute; bottom: 14px; left: 50%; transform: translateX(-50%); font-size: 12px; color: rgba(255,255,255,.9); background: rgba(0,0,0,.25); padding: 6px 10px; border-radius: 999px; }
</style>
