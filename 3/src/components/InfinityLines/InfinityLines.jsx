import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {isNumber, name} from '../../helpers';

import './InfinityLines.styl';

import Input from '../Input';

class InfinityLines extends Component {
    constructor(props) {
        super(props);
        this.state = {
            matrix: Array.apply(null, {
                length: this.props.countRows
            }).map((_, i) => Array.apply(null, {
                length: this.props.countColumns
            }).map((_, j) => (i === j ? '1' : '0')))
        };
    }

    componentDidMount() {
        this.props.setData(this.state.matrix);
    }

    componentDidUpdate(prevProps, prevState) {
        let flag = false;
        if (prevProps.countRows !== this.props.countRows) {
            flag = true;
            for (let i = prevProps.countRows; i < this.props.countRows; ++i) {
                this.state.matrix.push(new Array(prevProps.countColumns).fill('0'));
                if (i < prevProps.countColumns)
                    this.state.matrix[i][i] = '1';
            }
            this.state.matrix.length = this.props.countRows;
            this.setState({
                matrix: this.state.matrix
            });
        }
        if (prevProps.countColumns !== this.props.countColumns) {
            flag = true;
            for (let i = 0; i < this.props.countRows; ++i) {
                for (let j = prevProps.countColumns; j < this.props.countColumns; ++j) {
                    this.state.matrix[i].push('0');
                    if (i === j)
                        this.state.matrix[i][i] = '1';
                }
                this.state.matrix[i].length = this.props.countColumns;
            }
        }
        if (flag) {
            this.setState({
                matrix: this.state.matrix
            });
            this.props.setData(this.state.matrix);
        }
    }

    onChange(key, value) {
        if (!isNumber(value))
            return;
        key = parseInt(key);

        if (this.props.normalize && Math.abs(value) > 1)
            return;

        let row = Math.trunc(key / this.state.matrix.length);
        let column = key % this.state.matrix.length;

        this.state.matrix[row][column] = this.state.matrix[column][row] = value;

        this.setState({
            matrix: this.state.matrix,
        });
        this.props.onChange(row, column, parseFloat(value));
    }

    render() {
        return (
            <div className={`${name(this)} ${this.props.class}`}>
                {this.state.matrix.map((row, rowInd) => {
                    return (
                        <div className={'row'} key={rowInd}>
                        {row.map((val, columnInd) => {
                            let isTriangleFlag =
                                this.props.isTriangle &&
                                rowInd >= columnInd;
                            return (<Input
                                class={`one columns`}
                                style={{
                                    marginBottom: 0,
                                    backgroundColor: isTriangleFlag ? '#EBEBE4' : '',
                                }}
                                key={rowInd*row.length + columnInd}
                                onChange={(event) =>
                                    this.onChange(
                                        rowInd*row.length + columnInd, //key
                                        event.target.value, //value
                                    )}
                                value={this.state.matrix[rowInd][columnInd]}
                                readOnly={isTriangleFlag}
                            />)
                        })}
                        </div>
                    )
                })}
            </div>
        )
    }
}

InfinityLines.propTypes = {
    countRows : PropTypes.number.isRequired,
    countColumns : PropTypes.number.isRequired,
    isTriangle : PropTypes.bool.isRequired,
    normalize : PropTypes.bool.isRequired,
    setData: PropTypes.func.isRequired,
};

InfinityLines.defaultProps = {
    countRows : 1,
    isTriangle : false,
    normalize : false,
    setData: (data) => console.log(data),
};

export default InfinityLines;