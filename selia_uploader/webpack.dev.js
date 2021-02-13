const path = require('path');
const webpack = require('webpack');

const TARGET_DIR = path.join(
    __dirname,
    'static',
    'selia_uploader',
    'js',
);

module.exports = {
    mode: 'development',
    entry: path.join(__dirname, '/app/index.js'),
    output: {
        filename: 'upload_app.js',
        path: TARGET_DIR,
        library: 'uploader',
        libraryTarget: 'var',
    },
    module: {
        rules: [
            {
                test: [/\.ts$/, /\.tsx$/],
                use: 'ts-loader',
                exclude: '/node_modules/',
            },
            {
                test: [/\.js$/, /\.jsx$/],
                exclude: /node_modules/,
                loader: 'babel-loader',
                options: {
                    presets: ['@babel/preset-env','@babel/preset-react'],
                    plugins: [
                        "@babel/plugin-proposal-class-properties",
                        "@babel/plugin-transform-runtime"
                    ]
                }
            },
            {
                test: /\.css$/i,
                use: ["css-loader"],
            }
        ],
    },
    resolve: {
        extensions: ['.js', '.jsx', '.ts', '.tsx'],
        alias: {
            buffer: 'buffer'
        }
    },
    plugins: [
        new webpack.ProvidePlugin({	      
          Buffer: ['buffer', 'Buffer'],
        })
    ],
    watch: true,
};
