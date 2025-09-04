const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false,  // 关闭保存时lint，这样可以先运行起来
  
  // 生产环境配置
  publicPath: process.env.NODE_ENV === 'production' ? './' : '/',
  
  // 输出目录
  outputDir: 'dist',
  
  // 静态资源目录
  assetsDir: 'static',
  
  // 开发服务器配置
  devServer: {
    client: {
      overlay: false  // 禁用ESLint错误覆盖
    },
    port: 8080,
    host: '0.0.0.0',  // 允许局域网访问
    allowedHosts: 'all',  // 允许所有主机访问
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  },
  
  // 生产环境优化
  productionSourceMap: false,
  
  // 构建优化
  configureWebpack: {
    optimization: {
      splitChunks: {
        chunks: 'all'
      }
    },
    module: {
      rules: [
        {
          test: /\.(pptx|ppt|docx|xlsx|pdf)$/,
          type: 'asset/resource',
          generator: {
            filename: 'static/media/[name].[hash:8][ext]'
          }
        }
      ]
    }
  },
  
  // 链式配置
  chainWebpack: config => {
    // 排除特定文件类型，避免webpack尝试解析内容
    config.module
      .rule('exclude-docs')
      .test(/\.(pptx|ppt|docx|xlsx|pdf)$/)
      .use('file-loader')
      .loader('file-loader')
      .options({
        name: 'static/media/[name].[hash:8].[ext]',
        esModule: false
      })
      .end()
  }
}) 