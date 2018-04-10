import { connect } from 'react-redux';
import InfinityLine from './InfinityLine';
import { createAction } from "../../actions";

const mapStateToProps = state => ({
    // defVal: this.props.defVal,
});

const mapDispatchToProps = dispatch => ({});

export default connect(mapStateToProps, mapDispatchToProps)(InfinityLine);
