module.exports = process.env.NODE_ENV === 'production' ?
    require('./webpack/production')({env: 'production'}) :
    require('./webpack/dev')({env: 'development'});