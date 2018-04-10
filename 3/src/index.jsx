import React from 'react';
import ReactDOM from 'react-dom';
import { AppContainer } from 'react-hot-loader';
import configureStore from './store';
import Root from './components/Root';

const store = configureStore();

const render = Component => ReactDOM.render(
    <AppContainer>
        <Component store={store} />
    </AppContainer>,
    document.getElementById('root'),
);

render(Root);

if (module.hot) module.hot.accept('./components/Root', () => render(Root));
