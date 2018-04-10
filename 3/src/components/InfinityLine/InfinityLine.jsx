import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {
    name,
    isNumber
} from '../../helpers';

import './InfinityLine.styl';

import Input from '../Input';

class InfinityLine extends Component {
    constructor(props) {
        super(props);
        this.state = {
            variables: new Array(this.props.countRandomVariables).fill(this.props.defVal.toString()),
        };
    }

    componentDidMount() {
        this.props.setData(this.state.variables);
    }

    componentDidUpdate(prevProps, prevState) {
        if (prevProps.countRandomVariables !== this.props.countRandomVariables) {
            for (let i = prevProps.countRandomVariables; i < this.props.countRandomVariables; ++i)
                this.state.variables.push(this.props.defVal.toString());
            this.state.variables.length = this.props.countRandomVariables;
            this.setState({
                variables: this.state.variables,
            });
            this.props.setData(this.state.variables);
        }
    }

    onChange(key, value) {
        if (!isNumber(value))
            return;
        key = parseInt(key);
        if (parseFloat(value) > this.props.infVal)
            this.state.variables[key] = value;
        this.setState({
            variables: this.state.variables,
        });
        this.props.onChange(key, parseFloat(value));
    }

    render() {
        return (
            <div className={`${name(this)} ${this.props.class}`}>
                {this.state.variables.map((val, ind) =>
                    (<Input
                        class={'one columns'}
                        key={ind}
                        onChange={event => this.onChange(ind, event.target.value)}
                        value={this.state.variables[ind]}
                    />)
                )}
            </div>
        )
    }
}

InfinityLine.propTypes = {
    countRandomVariables : PropTypes.number.isRequired,
    setData: PropTypes.func.isRequired,
    defVal: PropTypes.number.isRequired,
    infVal: PropTypes.number.isRequired,
};

InfinityLine.defaultProps = {
    countRandomVariables : 1,
    setData: (data) => console.log(data),
    defVal: 0,
    infVal: -1 / 0.0,
};

export default InfinityLine;