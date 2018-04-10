import { applyMiddleware } from 'redux';
import multi from 'redux-multi';
import { middleware as fetchMiddleware } from 'react-redux-fetch';

const middleware = [
    //add middleware
];

if (process.env.NODE_ENV == 'development') {
    const logger = require('./logger').default;

    middleware.push(logger);
}

export default applyMiddleware(
    ...[
        fetchMiddleware,
        ...middleware,
        multi]
)