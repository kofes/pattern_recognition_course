const webpack = require('webpack');
const path = require('path');
const webpackMerge = require('webpack-merge');

const commonConfig = require('./common');

const ENV = process.env.ENV = process.env.NODE_ENV = 'development';

const BUILD_DIR = path.resolve(__dirname, '../dev-build');
const SRC_DIR = path.resolve(__dirname, '../src');

module.exports = config => webpackMerge(commonConfig({env: ENV}), {
    entry: [
        'react-hot-loader/patch',
        `${SRC_DIR}/index.jsx`
    ],
    context: BUILD_DIR,
    devtool: 'cheap-module-eval-source-map',
    output: {
        path: BUILD_DIR,
    },
    devServer: {
        hot: true,
        inline: true,
        historyApiFallback: true,
    },
    plugins: [
        new webpack.HotModuleReplacementPlugin()
    ]
});