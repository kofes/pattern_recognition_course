import { connect } from 'react-redux';
import InfinityLines from './InfinityLines';
import { createAction } from "../../actions";

const mapStateToProps = state => ({
    value: this.props.value,
    isTriangle: this.props.isTriangle,
});

const mapDispatchToProps = dispatch => ({});

export default connect(mapStateToProps, mapDispatchToProps)(InfinityLines);
