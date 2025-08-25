<template>
  <div class="home-container">
    <canvas id="canv"></canvas>
    <div class="content">
      <div class="title">
        生物世界
      </div>
      <router-link to="/chat" class="button">
        开始探索
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'

onMounted(() => {
  const canvas = document.getElementById('canv') as HTMLCanvasElement
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  let w = window.innerWidth
  let h = window.innerHeight
  canvas.width = w
  canvas.height = h

  const num = 200
  const max = 100
  let _x = 0
  let _y = 0
  let _z = 150

  const dtr = (d: number) => d * Math.PI / 180
  const rnd = () => Math.sin(Math.floor(Math.random() * 360) * Math.PI / 180)

  const cam = {
    obj: { x: _x, y: _y, z: _z },
    dest: { x: 0, y: 0, z: 1 },
    dist: { x: 0, y: 0, z: 200 },
    ang: { cplane: 0, splane: 0, ctheta: 0, stheta: 0 },
    zoom: 1,
    disp: { x: w / 2, y: h / 2, z: 0 },
    upd: function() {
      this.dist.x = this.dest.x - this.obj.x
      this.dist.y = this.dest.y - this.obj.y
      this.dist.z = this.dest.z - this.obj.z
      this.ang.cplane = -this.dist.z / Math.sqrt(this.dist.x * this.dist.x + this.dist.z * this.dist.z)
      this.ang.splane = this.dist.x / Math.sqrt(this.dist.x * this.dist.x + this.dist.z * this.dist.z)
      this.ang.ctheta = Math.sqrt(this.dist.x * this.dist.x + this.dist.z * this.dist.z) / 
                        Math.sqrt(this.dist.x * this.dist.x + this.dist.y * this.dist.y + this.dist.z * this.dist.z)
      this.ang.stheta = -this.dist.y / Math.sqrt(this.dist.x * this.dist.x + this.dist.y * this.dist.y + this.dist.z * this.dist.z)
    }
  }

  const trans = {
    parts: {
      sz: (p: any, sz: any) => ({ x: p.x * sz.x, y: p.y * sz.y, z: p.z * sz.z }),
      rot: {
        x: (p: any, rot: any) => ({
          x: p.x,
          y: p.y * Math.cos(dtr(rot.x)) - p.z * Math.sin(dtr(rot.x)),
          z: p.y * Math.sin(dtr(rot.x)) + p.z * Math.cos(dtr(rot.x))
        }),
        y: (p: any, rot: any) => ({
          x: p.x * Math.cos(dtr(rot.y)) + p.z * Math.sin(dtr(rot.y)),
          y: p.y,
          z: -p.x * Math.sin(dtr(rot.y)) + p.z * Math.cos(dtr(rot.y))
        }),
        z: (p: any, rot: any) => ({
          x: p.x * Math.cos(dtr(rot.z)) - p.y * Math.sin(dtr(rot.z)),
          y: p.x * Math.sin(dtr(rot.z)) + p.y * Math.cos(dtr(rot.z)),
          z: p.z
        })
      },
      pos: (p: any, pos: any) => ({ x: p.x + pos.x, y: p.y + pos.y, z: p.z + pos.z })
    },
    pov: {
      plane: (p: any) => ({
        x: p.x * cam.ang.cplane + p.z * cam.ang.splane,
        y: p.y,
        z: p.x * -cam.ang.splane + p.z * cam.ang.cplane
      }),
      theta: (p: any) => ({
        x: p.x,
        y: p.y * cam.ang.ctheta - p.z * cam.ang.stheta,
        z: p.y * cam.ang.stheta + p.z * cam.ang.ctheta
      }),
      set: (p: any) => ({
        x: p.x - cam.obj.x,
        y: p.y - cam.obj.y,
        z: p.z - cam.obj.z
      })
    },
    persp: (p: any) => ({
      x: p.x * cam.dist.z / p.z * cam.zoom,
      y: p.y * cam.dist.z / p.z * cam.zoom,
      z: p.z * cam.zoom,
      p: cam.dist.z / p.z
    }),
    disp: (p: any, disp: any) => ({
      x: p.x + disp.x,
      y: -p.y + disp.y,
      z: p.z + disp.z,
      p: p.p
    }),
    steps: (_obj_: any, sz: any, rot: any, pos: any, disp: any) => {
      let _args = trans.parts.sz(_obj_, sz)
      _args = trans.parts.rot.x(_args, rot)
      _args = trans.parts.rot.y(_args, rot)
      _args = trans.parts.rot.z(_args, rot)
      _args = trans.parts.pos(_args, pos)
      _args = trans.pov.plane(_args)
      _args = trans.pov.theta(_args)
      _args = trans.pov.set(_args)
      _args = trans.persp(_args)
      _args = trans.disp(_args, disp)
      return _args
    }
  }

  class ThreeD {
    transIn: any
    transOut: any
    constructor(param: any) {
      this.transIn = {}
      this.transOut = {}
      this.transIn.vtx = param.vtx
      this.transIn.sz = param.sz
      this.transIn.rot = param.rot
      this.transIn.pos = param.pos
    }
    vupd() {
      this.transOut = trans.steps(
        this.transIn.vtx,
        this.transIn.sz,
        this.transIn.rot,
        this.transIn.pos,
        cam.disp
      )
    }
  }

  class Build {
    canvas: HTMLCanvasElement
    ctx: CanvasRenderingContext2D
    vel: number
    lim: number
    diff: number
    initPos: number
    toX: number
    toY: number
    varr: ThreeD[]
    calc: any[]
    rotObj: any
    objSz: any

    constructor() {
      this.vel = 0.04
      this.lim = 360
      this.diff = 200
      this.initPos = 100
      this.toX = _x
      this.toY = _y
      this.go()
    }

    go() {
      this.canvas = canvas
      this.ctx = ctx
      this.ctx.globalCompositeOperation = 'source-over'
      this.varr = []
      this.calc = []

      for (let i = 0; i < num; i++) {
        this.add()
      }

      this.rotObj = { x: 0, y: 0, z: 0 }
      this.objSz = { x: w / 5, y: h / 5, z: w / 5 }
    }

    add() {
      this.varr.push(new ThreeD({
        vtx: { x: rnd(), y: rnd(), z: rnd() },
        sz: { x: 0, y: 0, z: 0 },
        rot: { x: 20, y: -20, z: 0 },
        pos: {
          x: this.diff * Math.sin(360 * Math.random() * Math.PI / 180),
          y: this.diff * Math.sin(360 * Math.random() * Math.PI / 180),
          z: this.diff * Math.sin(360 * Math.random() * Math.PI / 180)
        }
      }))
      this.calc.push({
        x: 360 * Math.random(),
        y: 360 * Math.random(),
        z: 360 * Math.random()
      })
    }

    upd() {
      cam.obj.x += (this.toX - cam.obj.x) * 0.05
      cam.obj.y += (this.toY - cam.obj.y) * 0.05
    }

    draw() {
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height)
      cam.upd()
      this.rotObj.x += 0.1
      this.rotObj.y += 0.1
      this.rotObj.z += 0.1

      for (let i = 0; i < this.varr.length; i++) {
        for (const val in this.calc[i]) {
          this.calc[i][val] += this.vel
          if (this.calc[i][val] > this.lim) this.calc[i][val] = 0
        }

        this.varr[i].transIn.pos = {
          x: this.diff * Math.cos(this.calc[i].x * Math.PI / 180),
          y: this.diff * Math.sin(this.calc[i].y * Math.PI / 180),
          z: this.diff * Math.sin(this.calc[i].z * Math.PI / 180)
        }
        this.varr[i].transIn.rot = this.rotObj
        this.varr[i].transIn.sz = this.objSz
        this.varr[i].vupd()
        if (this.varr[i].transOut.p < 0) continue

        const g = this.ctx.createRadialGradient(
          this.varr[i].transOut.x,
          this.varr[i].transOut.y,
          this.varr[i].transOut.p,
          this.varr[i].transOut.x,
          this.varr[i].transOut.y,
          this.varr[i].transOut.p * 2
        )
        this.ctx.globalCompositeOperation = 'lighter'
        g.addColorStop(0, 'hsla(255, 255%, 255%, 1)')
        g.addColorStop(0.5, `hsla(${i + 2}, 85%, 40%, 1)`)
        g.addColorStop(1, `hsla(${i}, 85%, 40%, 0.5)`)
        this.ctx.fillStyle = g
        this.ctx.beginPath()
        this.ctx.arc(
          this.varr[i].transOut.x,
          this.varr[i].transOut.y,
          this.varr[i].transOut.p * 2,
          0,
          Math.PI * 2,
          false
        )
        this.ctx.fill()
        this.ctx.closePath()
      }
    }

    anim() {
      this.upd()
      this.draw()
      requestAnimationFrame(() => this.anim())
    }

    run() {
      this.anim()

      window.addEventListener('mousemove', (e) => {
        this.toX = (e.clientX - this.canvas.width / 2) * -0.8
        this.toY = (e.clientY - this.canvas.height / 2) * 0.8
      })

      window.addEventListener('touchmove', (e) => {
        e.preventDefault()
        this.toX = (e.touches[0].clientX - this.canvas.width / 2) * -0.8
        this.toY = (e.touches[0].clientY - this.canvas.height / 2) * 0.8
      })

      window.addEventListener('mousedown', () => {
        for (let i = 0; i < 100; i++) {
          this.add()
        }
      })

      window.addEventListener('touchstart', (e) => {
        e.preventDefault()
        for (let i = 0; i < 100; i++) {
          this.add()
        }
      })
    }
  }

  const app = new Build()
  app.run()

  window.addEventListener('resize', () => {
    w = window.innerWidth
    h = window.innerHeight
    canvas.width = w
    canvas.height = h
  })
})
</script>

<style scoped>
.home-container {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  background: #ffffff;
}

#canv {
  position: absolute;
  z-index: 1;
  width: 100vw;
  height: 100vh;
  left: 0;
  top: 0;
}

.content {
  position: absolute;
  z-index: 2;
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  text-align: center;
  padding-top: 20vh;
}

.title {
  font-size: 160px;
  margin-bottom: 40px;
  background: linear-gradient(
    to right,
    rgba(255, 0, 0, 0.4),
    rgba(255, 165, 0, 0.4),
    rgba(255, 255, 0, 0.4),
    rgba(0, 255, 0, 0.4),
    rgba(0, 0, 255, 0.4),
    rgba(75, 0, 130, 0.4),
    rgba(238, 130, 238, 0.4)
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
}

.button {
  padding: 20px 45px;
  background-color: rgba(232, 82, 32, 0.637);
  color: white;
  border: none;
  border-radius: 20px;
  font-size: 25px;
  text-decoration: none;
  transition: background-color 0.3s;
  cursor: pointer;
  margin-top: 20vh;
}

.button:hover {
  background-color: #ff4500;
}

@media (max-width: 768px) {
  .title {
    font-size: 80px;
  }
  
  .button {
    padding: 15px 30px;
    font-size: 20px;
  }
}
</style> 