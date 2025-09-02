<template>
  <div class="cropper-container">
    <input class="file-input" type="file" accept="image/*" @change="onSelect" />
    <div v-if="imageUrl" class="canvas-wrap">
      <canvas ref="canvas" :width="size" :height="size"></canvas>
      <div class="controls">
        <el-slider v-model="scale" :min="0.5" :max="3" :step="0.01" style="width:220px" />
        <el-button size="small" @click="emitCancel">取消</el-button>
        <el-button type="primary" size="small" @click="emitDone">确定</el-button>
      </div>
    </div>
    <div v-else class="hint">选择图片进行裁剪</div>
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref, watch, nextTick } from 'vue'

const props = defineProps({ size: { type: Number, default: 240 } })
const emit = defineEmits(['cancel', 'done'])

const canvas = ref(null)
const ctxRef = ref(null)
const image = ref(null)
const imageUrl = ref('')
const scale = ref(1)
const offsetX = ref(0)
const offsetY = ref(0)

function onSelect(e) {
  const file = e.target.files && e.target.files[0]
  if (!file) return
  const url = URL.createObjectURL(file)
  imageUrl.value = url
  const img = new Image()
  img.onload = () => {
    image.value = img
    offsetX.value = 0
    offsetY.value = 0
    scale.value = 1
    draw()
  }
  img.src = url
}

function draw() {
  const cvs = canvas.value
  if (!cvs) return
  const size = cvs.width
  const ctx = ctxRef.value || (ctxRef.value = cvs.getContext('2d'))
  ctx.clearRect(0, 0, size, size)
  // draw image with pan/zoom
  if (image.value) {
    const img = image.value
    const iw = img.width
    const ih = img.height
    const baseScale = Math.max(size / iw, size / ih)
    const s = baseScale * scale.value
    const drawW = iw * s
    const drawH = ih * s
    const dx = (size - drawW) / 2 + offsetX.value
    const dy = (size - drawH) / 2 + offsetY.value
    ctx.save()
    ctx.beginPath()
    ctx.arc(size / 2, size / 2, size / 2, 0, Math.PI * 2)
    ctx.closePath()
    ctx.clip()
    ctx.drawImage(img, dx, dy, drawW, drawH)
    ctx.restore()
    // overlay ring
    ctx.beginPath()
    ctx.arc(size / 2, size / 2, size / 2 - 1, 0, Math.PI * 2)
    ctx.strokeStyle = 'rgba(0,0,0,.15)'
    ctx.lineWidth = 2
    ctx.stroke()
  }
  // mask outside circle
  ctx.save()
  ctx.globalCompositeOperation = 'destination-over'
  ctx.fillStyle = 'rgba(0,0,0,.25)'
  ctx.fillRect(0, 0, size, size)
  ctx.globalCompositeOperation = 'destination-out'
  ctx.beginPath()
  ctx.arc(size / 2, size / 2, size / 2, 0, Math.PI * 2)
  ctx.fill()
  ctx.restore()
}

let dragging = false
let startX = 0
let startY = 0

function onPointerDown(ev) {
  if (!image.value) return
  dragging = true
  startX = ev.clientX
  startY = ev.clientY
  if (canvas.value) canvas.value.style.cursor = 'grabbing'
}
function onPointerMove(ev) {
  if (!dragging) return
  offsetX.value += ev.clientX - startX
  offsetY.value += ev.clientY - startY
  startX = ev.clientX
  startY = ev.clientY
  enforceBounds()
  draw()
}
function onPointerUp() { dragging = false; if (canvas.value) canvas.value.style.cursor = 'grab' }

function onDblClick(ev) {
  if (!image.value || !canvas.value) return
  const cvs = canvas.value
  const size = cvs.width
  const iw = image.value.width
  const ih = image.value.height
  const baseScale = Math.max(size / iw, size / ih)
  const s = baseScale * scale.value
  const drawW = iw * s
  const drawH = ih * s
  const dxBefore = (size - drawW) / 2 + offsetX.value
  const dyBefore = (size - drawH) / 2 + offsetY.value
  const u = (ev.offsetX - dxBefore) / drawW
  const v = (ev.offsetY - dyBefore) / drawH
  const dxAfter = size / 2 - u * drawW
  const dyAfter = size / 2 - v * drawH
  offsetX.value = dxAfter - (size - drawW) / 2
  offsetY.value = dyAfter - (size - drawH) / 2
  enforceBounds()
  draw()
}

function enforceBounds() {
  const cvs = canvas.value
  if (!cvs || !image.value) return
  const size = cvs.width
  const r = size / 2
  const iw = image.value.width
  const ih = image.value.height
  const baseScale = Math.max(size / iw, size / ih)
  const s = baseScale * scale.value
  const drawW = iw * s
  const drawH = ih * s
  let dx = (size - drawW) / 2 + offsetX.value
  let dy = (size - drawH) / 2 + offsetY.value
  const minLeft = size / 2 - r // = 0
  const maxRight = size / 2 + r // = size
  // ensure image covers circle bounding box fully
  if (dx > minLeft) { offsetX.value -= (dx - minLeft) }
  if (dx + drawW < maxRight) { offsetX.value += (maxRight - (dx + drawW)) }
  if (dy > minLeft) { offsetY.value -= (dy - minLeft) }
  if (dy + drawH < maxRight) { offsetY.value += (maxRight - (dy + drawH)) }
}

watch([scale, imageUrl], () => { enforceBounds(); draw() })

function wheelHandler(ev) {
  if (!image.value || !canvas.value) return
  ev.preventDefault()
  const cvs = canvas.value
  const size = cvs.width
  const cx = ev.offsetX
  const cy = ev.offsetY
  const iw = image.value.width
  const ih = image.value.height
  const baseScale = Math.max(size / iw, size / ih)
  const sBefore = baseScale * scale.value
  const drawWBefore = iw * sBefore
  const drawHBefore = ih * sBefore
  const dxBefore = (size - drawWBefore) / 2 + offsetX.value
  const dyBefore = (size - drawHBefore) / 2 + offsetY.value
  const u = (cx - dxBefore) / drawWBefore
  const v = (cy - dyBefore) / drawHBefore
  const factor = Math.exp(-ev.deltaY * 0.0015)
  const nextScale = Math.min(3, Math.max(0.5, scale.value * factor))
  const sAfter = baseScale * nextScale
  const drawWAfter = iw * sAfter
  const drawHAfter = ih * sAfter
  const dxAfter = cx - u * drawWAfter
  const dyAfter = cy - v * drawHAfter
  offsetX.value = dxAfter - (size - drawWAfter) / 2
  offsetY.value = dyAfter - (size - drawHAfter) / 2
  scale.value = nextScale
  enforceBounds()
  draw()
}

function attachCanvasListeners() {
  const cvs = canvas.value
  if (!cvs) return
  cvs.addEventListener('pointerdown', onPointerDown)
  window.addEventListener('pointermove', onPointerMove)
  window.addEventListener('pointerup', onPointerUp)
  cvs.addEventListener('dblclick', onDblClick)
  cvs.addEventListener('wheel', wheelHandler, { passive: false })
  cvs.style.cursor = 'grab'
}

function detachCanvasListeners() {
  const cvs = canvas.value
  if (!cvs) return
  cvs.removeEventListener('pointerdown', onPointerDown)
  window.removeEventListener('pointermove', onPointerMove)
  window.removeEventListener('pointerup', onPointerUp)
  cvs.removeEventListener('dblclick', onDblClick)
  cvs.removeEventListener('wheel', wheelHandler)
}

onMounted(() => {
  if (imageUrl.value) {
    nextTick(() => attachCanvasListeners())
  }
})

onBeforeUnmount(() => {
  detachCanvasListeners()
})

watch(imageUrl, (val) => {
  if (val) {
    nextTick(() => attachCanvasListeners())
  } else {
    detachCanvasListeners()
  }
})

function emitCancel() { emit('cancel') }
function emitDone() {
  const cvs = canvas.value
  if (!cvs) return emit('cancel')
  cvs.toBlob((blob) => {
    emit('done', blob)
  }, 'image/png')
}
</script>

<style scoped>
.cropper-container{ display:flex; flex-direction: column; align-items: center; gap: 10px; }
.file-input{ margin-bottom: 8px; }
.canvas-wrap{ position: relative; display:flex; flex-direction: column; align-items: center; gap: 10px; }
canvas{ border-radius: 50%; box-shadow: 0 6px 20px rgba(0,0,0,.12); }
.controls{ display:flex; align-items:center; gap:10px; }
.hint{ font-size: 12px; color: #909399; }
</style>

