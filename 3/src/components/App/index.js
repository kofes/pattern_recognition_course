import { connect } from 'react-redux';
import App from './App';
import { createAction } from "../../actions";

const mapStateToProps = state => ({});

const mapDispatchToProps = dispatch => ({
    dispatch: type => dispatch(createAction(type)),
});

export default connect(mapStateToProps, mapDispatchToProps)(App);
