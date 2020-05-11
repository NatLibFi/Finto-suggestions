module.exports = {
  devServer: {
    port: 8040,
    public: '0.0.0.0',
    disableHostCheck: false,
    watchOptions: {
      poll: 1000
    }
  }
};

// see -> https://github.com/lincenying/vue-cli/blob/master/docs/proxy.md
// see -> https://webpack.js.org/configuration/dev-server/
