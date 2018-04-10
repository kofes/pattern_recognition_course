import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {name} from '../../helpers';

import './Input.styl';

class Input extends Component {
    constructor(props) {
        super(props);
    }

    onChange(event) {
        this.props.onChange(event);
    }

    render() {
        return (
            <div className={`${name(this)}`}>
                <input
                    className={`u-full-width ${this.props.class}`}
                    style={{...this.props.style}}
                    onChange={(event) => this.onChange(event)}
                    value={this.props.value}
                    readOnly={this.props.readOnly}
                />
            </div>
        )
    }
}

Input.propTypes = {
    style: PropTypes.object.isRequired,
    readOnly: PropTypes.bool.isRequired,
    value: PropTypes.oneOfType([
        PropTypes.string.isRequired,
        PropTypes.number.isRequired
    ]),
    onChange: PropTypes.func.isRequired,
};

Input.defaultProps = {
    style: {},
    readOnly: false,
    value: '0',
    onChange: (event) => console.log(event),
};

export default Input;