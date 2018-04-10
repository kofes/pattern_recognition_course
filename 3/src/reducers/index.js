import { combineReducers } from 'redux';
import { reducer as fetchReducer } from 'react-redux-fetch';

const reducers = {
    //add reducers
};

export default combineReducers({
    ...reducers,
    fetchReducer,
});