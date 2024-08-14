export default {
  entry: './src/main.js',
  mode: 'production',
  //mode: 'development',
  optimization: {
    usedExports: true,
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [ 'style-loader', 'css-loader' ]
      },
      {
        test: /datatables\.net.*.js$/,
        use: [{
          loader: 'imports-loader',
          options: {
            additionalCode: 'var define = false; /* Disable AMD for misbehaving libraries */'
          }
        }]
      }
    ]
  }
}
