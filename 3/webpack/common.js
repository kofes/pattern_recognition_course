const webpack = require('webpack');
const path = require('path');

const HtmlWebpackPlugin = require('html-webpack-plugin');

const BUILD_DIR = path.resolve(__dirname, '../build');
const SRC_DIR = path.resolve(__dirname, '../src');

const PROJECT_NAME = 'JECT';

module.exports = config => ({
    context: BUILD_DIR,
    entry: `${SRC_DIR}/index.jsx`,
    output: {
        path: BUILD_DIR,
        filename: 'bundle.js',
    },
    resolve: {
        extensions: ['.js', '.jsx']
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                include: SRC_DIR,
                loader: 'babel-loader',
                exclude: '/node_modules/',
            }, {
                test: /\.html$/,
                loader: "file?name=[name].[ext]"
            }, {
                test   : /\.woff/,
                loader : 'url?prefix=font/&limit=10000&mimetype=application/font-woff'
            }, {
                test   : /\.ttf/,
                loader : 'file?prefix=font/'
            }, {
                test   : /\.eot/,
                loader : 'file?prefix=font/'
            }, {
                test: /\.(png|jpg|gif|svg)$/,
                loader: 'file-loader',
                options: {
                    name: '[name].[ext]?[hash]'
                }
            }, {
                test: /\.css$/,
                loader: 'style-loader!css-loader'
            }, {
                test: /\.styl$/,
                loader: 'style-loader!css-loader!stylus-loader'
            },
        ],
    },
    plugins: [
        new webpack.DefinePlugin({
            'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV || 'development')
        }),
        new webpack.NoEmitOnErrorsPlugin(),
        new HtmlWebpackPlugin({
            title: PROJECT_NAME,
            filename: 'index.html',
            favicon: `${SRC_DIR}/favicon.ico`,
            template: `${SRC_DIR}/index.ejs`,
        }),
    ]
});