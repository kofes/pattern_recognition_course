import React from 'react';
import { Provider } from 'react-redux';
import PropTypes from 'prop-types';
import LocalRouter from '../LocalRouter';

const Root = ({ store }) => (
    <Provider store={store}>
        <LocalRouter />
    </Provider>
);

Root.propTypes = {
    store: PropTypes.shape({
        getState: PropTypes.func.isRequired,
        dispatch: PropTypes.func.isRequired,
    }).isRequired,
};

export default Root;
