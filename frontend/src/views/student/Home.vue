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
import { useRouter } from 'vue-router'
import AiAssistant from '../../components/AiAssistant.vue'

const wrapRef = ref(null)
const canvasRef = ref(null)

// 资源与链接（将 0.png-7.png 放在 src/assets/img/ 下）
const ctx = require.context('../../assets/img', false, /\.(png|jpe?g)$/)
const imgMap = {}
ctx.keys().forEach(k => { imgMap[k.replace('./','')] = ctx(k) })
const fallbackImg = imgMap['1.png'] || imgMap['Logo.png'] || ''
const imageFiles = Array.from({ length: 8 }, (_, i) => imgMap[`${i}.png`] || imgMap[`${i}.jpg`] || fallbackImg)
// 跳转到学生端关卡路由
const links = [
  '/StudentSide/levelt/level0',
  '/StudentSide/levelt/level1',
  '/StudentSide/levelt/level2',
  '/StudentSide/levelt/level3',
  '/StudentSide/levelt/level4',
  '/StudentSide/levelt/level5',
  '/StudentSide/levelt/level6',
  '/StudentSide/levelt/level7'
]
// 每张图片下方标题
const titles = [
  '细胞的组成',
  '细胞的结构与功能',
  '细胞的物质输入和输出',
  '酶和ATP',
  '细胞呼吸',
  '光合作用',
  '细胞的增殖和减数分裂',
  '细胞的分化、衰老、凋亡和癌变'
]
const bgColors = ['#f5f7fa']

let scene, camera, renderer, group
let textures = []
let meshes = []
let labelMeshes = []
let animId
const raycaster = new THREE.Raycaster()
const pointer = new THREE.Vector2()
let hoveredIndex = -1
const isDragging = ref(false)
const router = useRouter()

// 旋转与交互状态
let angle = 0
let targetAngle = 0
let startX = 0
let startAngleSnapshot = 0
let activeIndex = 0

function lerp(a, b, t){
  return a + (b - a) * t
}

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
    img.src = typeof src === 'string' ? src : (src && src.default) ? src.default : src
  })
}

function createLabelTexture(text){
  const padX = 24, padY = 10
  const fontSize = 60
  const canvas = document.createElement('canvas')
  const ctx2d = canvas.getContext('2d')
  ctx2d.font = `${fontSize}px \\"Segoe UI\\", Arial, sans-serif`
  const metrics = ctx2d.measureText(text)
  const textW = Math.ceil(metrics.width)
  const w = textW + padX * 2
  const h = fontSize + padY * 2
  canvas.width = w
  canvas.height = h
  // 仅绘制文字，背景保持透明，标记文字颜色
  ctx2d.font = `${fontSize}px \\"Segoe UI\\", Arial, sans-serif`
  ctx2d.fillStyle = '#000000'
  ctx2d.textBaseline = 'middle'
  ctx2d.fillText(text, padX, h/2)
  const tex = new THREE.CanvasTexture(canvas)
  tex.anisotropy = 4
  // 水平镜像文字贴图（左右翻转显示）
  tex.center.set(0.5, 0.5)
  tex.repeat.x = -1
  tex.needsUpdate = true
  return { texture: tex, width: w, height: h }
}

async function init() {
  scene = new THREE.Scene()
  const w = wrapRef.value.clientWidth
  const h = wrapRef.value.clientHeight
  const fov = 35
  camera = new THREE.PerspectiveCamera(fov, w/h, 0.1, 100)
  camera.position.set(0, 1.4, 5.5)
  camera.lookAt(0, 1.4, 0)

  renderer = new THREE.WebGLRenderer({ canvas: canvasRef.value, antialias: true, alpha: true })
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
  renderer.setSize(w, h)
  renderer.shadowMap.enabled = true
  renderer.shadowMap.type = THREE.PCFSoftShadowMap
  
  group = new THREE.Group()
  scene.add(group)
  group.position.y = 0.3
  
  const amb = new THREE.AmbientLight(0xffffff, 2.5)
  scene.add(amb)
  const dirLight = new THREE.DirectionalLight(0xffffff, 0.7)
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
  const hemi = new THREE.HemisphereLight(0xffffff, 0x444444, 0.4)
  scene.add(hemi)
  const groundGeo = new THREE.CircleGeometry(3.0, 64)
  const groundMat = new THREE.ShadowMaterial({ opacity: 0.18 })
  const ground = new THREE.Mesh(groundGeo, groundMat)
  ground.rotation.x = -Math.PI / 2
  ground.position.set(0, 0.9, 0)
  ground.scale.set(1.6, 1, 1)
  ground.receiveShadow = true
  scene.add(ground)
  
  const circUrls = await Promise.all(imageFiles.map(src => toCircleDataURL(src)))
  const loader = new THREE.TextureLoader()
  textures = circUrls.map(u => loader.load(u || fallbackImg))
  textures.forEach(tex => { if (!tex) return; tex.center.set(0.5,0.5); tex.repeat.x = -1; tex.needsUpdate = true })

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
    group.add(mesh)
    return mesh
  })
  // 创建文字标签
  labelMeshes = titles.map((t, i) => {
    const { texture, width, height } = createLabelTexture(t)
    const scaleW = 0.9
    const pxToWorld = (planeSize * scaleW) / (512) // 以图片尺寸基准估算
    const wWorld = width * pxToWorld
    const hWorld = height * pxToWorld
    const geo = new THREE.PlaneGeometry(wWorld, hWorld)
    const mat = new THREE.MeshBasicMaterial({ map: texture, transparent: true, depthWrite: false, depthTest: false, side: THREE.DoubleSide })
    const m = new THREE.Mesh(geo, mat)
    const theta = (i / count) * Math.PI * 2
    const x = Math.cos(theta) * radius
    const z = Math.sin(theta) * radius
    m.position.set(x, 0.75, z) // 图片下方
    m.lookAt(0, 1.4, 0)
    m.renderOrder = 999
    group.add(m)
    return m
  })

  setBgColor(activeIndex)

  const canvas = canvasRef.value
  canvas.addEventListener('mousedown', onDown)
  canvas.addEventListener('mouseup', onUp)
  canvas.addEventListener('mouseleave', onUp)
  canvas.addEventListener('mousemove', onMouseMove)
  canvas.addEventListener('touchstart', onTouchStart, { passive: true })
  canvas.addEventListener('touchend', onTouchEnd, { passive: true })
  canvas.addEventListener('touchcancel', onTouchEnd, { passive: true })
  canvas.addEventListener('touchmove', onTouchMove, { passive: true })
  canvas.addEventListener('dblclick', onDblClickOpen)
  window.addEventListener('resize', onResize)

  animate()
}

function onDblClickOpen(){
  const m = meshes[activeIndex]
  if (!m) return
  const camForward = new THREE.Vector3(0,0,-1).applyQuaternion(camera.quaternion)
  const front = camForward.dot(new THREE.Vector3().subVectors(m.position, camera.position).normalize()) > 0
  if (!front) return
  const url = links[activeIndex]
  if (url) router.push(url)
}

function animate(){
  animId = requestAnimationFrame(animate)
  if (!isDragging.value) { targetAngle += 0.0008 }
  angle = lerp(angle, targetAngle, 0.06)
  group.rotation.y = angle
  const camForward = new THREE.Vector3(0,0,-1).applyQuaternion(camera.quaternion)
  meshes.forEach((m, i) => {
    const toMesh = new THREE.Vector3().subVectors(m.position, camera.position).normalize()
    const front = camForward.dot(toMesh) > 0
    const mat = m.material
    mat.opacity = front ? 1.0 : 0.12
    const targetScale = (i === hoveredIndex && front) ? 1.4 : 1.0
    m.scale.x = lerp(m.scale.x, targetScale, 0.2)
    m.scale.y = lerp(m.scale.y, targetScale, 0.2)
    // 文本标签与图片同步透明度与缩放
    const label = labelMeshes[i]
    if (label){
      const lm = label.material
      lm.opacity = front ? 1.0 : 0.12
      const labelScale = (i === hoveredIndex && front) ? 1.12 : 1.0
      label.scale.x = lerp(label.scale.x || 1, labelScale, 0.2)
      label.scale.y = lerp(label.scale.y || 1, labelScale, 0.2)
      // 让文字随图片方向转动（不强制面向相机）
    }
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
