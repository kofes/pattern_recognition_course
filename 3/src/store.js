import { createStore, compose } from 'redux';
import reducers from './reducers';
import middleware from './middleware';

const configureStore = () => {
    const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
    const store = createStore(reducers, composeEnhancers(middleware));

    if (module.hot) module.hot.accept('./reducers/', () => store.replaceReducer(reducers));

    return store;
};

export default configureStore;
