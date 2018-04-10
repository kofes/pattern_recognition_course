// React
import React, {Component} from 'react';
import PropTypes from 'prop-types';

// Own
import {
    name,
    isNumber,
    numberToWord,
    norm2DDistribution,
    if_then,
    translateMatrix,
} from '../../helpers';
import InfinityLine from '../InfinityLine';
import Input from "../Input/Input";
import InfinityLines from "../InfinityLines/InfinityLines";

// Local member
import './App.styl';

// 3d party
import Select from 'react-select';
import 'react-select/dist/react-select.css';
import Plot from 'react-plotly.js';
import '../../css/normalize.css';
import '../../css/skeleton.css';

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            countRandomVariables: 2,
            selected: [],

            data: {
                size: 200,
                x: [],
                y: [],
                z: [],
            },

            mean: [],
            D: [],
            r: [],
            rChanged: {},

            plotType: {label: 'surface'},
            plotTypes: [
                'surface',
                'isolines'
            ],

            generated: {
                size: 0,
                dots: [],
            },

            mean_t: [],
            D_t: [],
            r_t: [],
        };
    }

    onChange(value) {
        if (!isNumber(value))
            return;
        value = parseInt(value);
        if (value < 0) return;
        value = value ? value : 1;

        this.setState({
            countRandomVariables: value
        });
    }

    onChangeGenSize(value) {
        if (!isNumber(value))
            return;
        value = parseInt(value);
        if (value < 0) return;
        // value = value ? value : 1;
        // console.log(value);
        this.setState({
            generated: {...this.state.generated, size: value}
        });
    }

    onSelect(ind, selectedElem) {
        if (selectedElem == null) return;
        let selected = [ ...this.state.selected ];
        selected[ind] = {...selected[ind], ...selectedElem};
        this.setState({ selected });
    }

    componentDidUpdate(prevProps, prevState) {
        let f_selectedChanged = false;
        let data = {...this.state.data};

        let sigma = !this.state.selected[0] ? (
            !this.state.selected[1] ? 1 :
                Math.sqrt(this.state.D[this.state.selected[1].value])
        ) : !this.state.selected[1] ? Math.sqrt(this.state.D[this.state.selected[0].value]) :
            Math.sqrt(Math.max(
                this.state.D[this.state.selected[0].value],
                this.state.D[this.state.selected[1].value]
            ));

        if (this.state.selected[0] && (
            prevState.selected[0] !== this.state.selected[0] ||
            prevState.D[this.state.selected[0].value] !== this.state.D[this.state.selected[0].value] ||
            prevState.mean[this.state.selected[0].value] !== this.state.mean[this.state.selected[0].value]
        )) {
            f_selectedChanged = true;
            data = {
                ...data,
                x: Array.apply(null, {
                    length: this.state.data.size
                }).map((_, v) => (
                    this.state.mean[this.state.selected[0].value] -
                    3 * sigma +
                    6 * sigma
                    * v / this.state.data.size
                ))
            };
        }

        if (this.state.selected[1] && (
            prevState.selected[1] !== this.state.selected[1] ||
            prevState.D[this.state.selected[1].value] !== this.state.D[this.state.selected[1].value] ||
            prevState.mean[this.state.selected[1].value] !== this.state.mean[this.state.selected[1].value]
        )) {
            f_selectedChanged = true;
            data = {
                ...data,
                y: Array.apply(null, {
                    length: this.state.data.size
                }).map((_, v) => (
                    this.state.mean[this.state.selected[1].value] -
                    3 * sigma +
                    6 * sigma
                    * v / this.state.data.size
                ))
            };
        }

        if (this.state.selected[0] && this.state.selected[1]) {
            let selectObjs = [{
                row: this.state.selected[0].value,
                column: this.state.selected[1].value
            }, {
                row: this.state.selected[1].value,
                column: this.state.selected[0].value
            }];

            if (f_selectedChanged ||
                JSON.stringify(selectObjs[0]) === JSON.stringify(this.state.rChanged) ||
                JSON.stringify(selectObjs[1]) === JSON.stringify(this.state.rChanged)
            ) {
                this.setState({rChanged: {}});
                f_selectedChanged = true;
                data = {...data,
                    z: Array.apply(null, {
                        length: this.state.data.size
                    }).map((_, x1) => (
                        Array.apply(null, {
                            length: this.state.data.size
                        }).map((_, x2) => norm2DDistribution(
                            this.state.mean[this.state.selected[0].value],
                            Math.sqrt(this.state.D[this.state.selected[0].value]),
                            this.state.mean[this.state.selected[1].value],
                            Math.sqrt(this.state.D[this.state.selected[1].value]),
                            this.state.r[this.state.selected[0].value][this.state.selected[1].value]
                        )(
                            this.state.mean[this.state.selected[0].value] -
                            3 * sigma +
                            6 * sigma
                            * x1 / this.state.data.size,
                            this.state.mean[this.state.selected[1].value] -
                            3 * sigma +
                            6 * sigma
                            * x2 / this.state.data.size
                        ))
                    ))
                };
            }
        }

        if (f_selectedChanged) this.setState({data});
        if (prevState.D !== this.state.D ||
            prevState.mean !== this.state.mean ||
            prevState.r !== this.state.r ||
            prevState.generated.size !== this.state.generated.size)
            this.generateDots();

        //    remake E^, r^, D^
        if (prevState.generated.dots !== this.state.generated.dots && this.state.generated.dots.length) {
            let sum = arr => arr.reduce((x, y) => x + y, 0);
            let mul = (arr1, arr2) => arr1.map((val, ind) => val * arr2[ind]);

            let mean_t = new Array(this.state.countRandomVariables);
            let D_t = new Array(this.state.countRandomVariables);
            let r_t = new Array(this.state.countRandomVariables);
            for (let i = 0; i < r_t.length; ++i)
                r_t[i] = new Array(this.state.countRandomVariables);
            for (let i = 0; i < this.state.countRandomVariables; ++i) {
                mean_t[i] = sum(this.state.generated.dots[i]) / this.state.generated.size;
                D_t[i] = sum(this.state.generated.dots[i].map(val => (val**2 - mean_t[i]**2))) / (this.state.generated.size - 1);
            }
            for (let i = 0; i < this.state.countRandomVariables; ++i)
                for (let j = 0; j < this.state.countRandomVariables; ++j) {
                    let x = this.state.generated.dots[i].map(val => val - mean_t[i]);
                    let y = this.state.generated.dots[j].map(val => val - mean_t[j]);
                    r_t[i][j] = sum(mul(x, y)) / (this.state.generated.size - 1) / Math.sqrt(D_t[i] * D_t[j]);
                }
            this.setState({mean_t, D_t, r_t});
        }
    }

    generateDots() {
        if (this.state.generated.size === 0) {
            this.setState({generated: {...this.state.generated, dots: []}});
            return;
        }
        let result = new Array(this.state.generated.size);
        let mat = translateMatrix(this.state.mean, this.state.D, this.state.r);
        console.log(mat);
        for (let i = 0; i < this.state.generated.size; ++i) {
            let vec = new Array(this.state.countRandomVariables);
            for (let k = 0; k < this.state.countRandomVariables; ++k) {
                let s = 0;
                let u, v;
                while (Math.abs(s - 0.5) >= 0.5) {
                    u = 2* Math.random() - 1;
                    v = 2 * Math.random() - 1;
                    s = u**2 + v**2
                }
                vec[k] = u * Math.sqrt(-2 * Math.log(s) / s);
                if (k !== this.state.countRandomVariables-1)
                    vec[k+1] = v * Math.sqrt(-2 * Math.log(s) / s);
            }
            result[i] = new Array(this.state.countRandomVariables);
            for (let k = 0; k < this.state.countRandomVariables; ++k) {
                result[i][k] = 0;
                for (let j = 0; j < this.state.countRandomVariables; ++j)
                    result[i][k] += mat[k][j] * vec[j];
                result[i][k] += this.state.mean[k];
            }
        }
        let transpose = m => m[0].map((x,i) => m.map(x => x[i]));
        result = transpose(result);
        console.log(result);
        this.setState({generated: {...this.state.generated, dots: result}});
    }

    render() {
        return (
            <div className={`${name(this)} container`} ref={it => {this.is = it}}>
                {/*Count variables*/}
                <div className={'row'}>
                    <label htmlFor={`${name(Input)}-${'countVariables'}`}>
                        Count variables:
                    </label>
                    <Input
                        class={'one columns'}
                        onChange={(event) => this.onChange(event.target.value)}
                        value={this.state.countRandomVariables}
                    />
                </div>

                {/*Mean variables*/}
                <label htmlFor={`${name(InfinityLine)}-${'meanVariables'}`}>
                    Mean variables:
                </label>
                <InfinityLine
                    class={'row'}
                    countRandomVariables={this.state.countRandomVariables}
                    setData={(data) => this.setState({mean: data.map((val) => parseFloat(val))})}
                    onChange={(ind, val) => {
                        let mean = [...this.state.mean];
                        mean[ind] = val;
                        this.setState({mean});
                    }}
                />

                {/*Normalized correlation matrix*/}
                <label htmlFor={`${name(InfinityLine)}-${'normalizedCorrelationInfinityLines'}`}>
                    Normalized correlation matrix:
                </label>
                <InfinityLines
                    countRows={this.state.countRandomVariables}
                    countColumns={this.state.countRandomVariables}
                    isTriangle={true}
                    normalize={true}
                    setData={(data) => this.setState({r: data.map((row) => row.map((val) => parseFloat(val)))})}
                    onChange={(row, column, val) => {
                        let r = [...this.state.r];
                        r[row][column] = r[column][row] = val;
                        this.setState({r, rChanged: {row, column}});
                    }}
                />

                {/*Dispersion vector*/}
                <label htmlFor={`${name(InfinityLine)}-${'dispersionVector'}`}>
                    Dispersion vector:
                </label>
                <InfinityLine
                    class={'row'}
                    defVal={1}
                    infVal={0}
                    countRandomVariables={this.state.countRandomVariables}
                    setData={(data) => this.setState({D: data.map((val) => parseFloat(val))})}
                    onChange={(ind, val) => {
                        let D = [...this.state.D];
                        D[ind] = val ? val : 1;
                        this.setState({D});
                    }}
                />

                {/*Elements selector*/}
                <label htmlFor={'selectors'}>
                    Select elements:
                </label>
                <div className={'row'} id={`${name(Select)}-${'selectors'}`}>
                    <Select
                        name={'first-elem'}
                        removeSelected={true}
                        className={'two columns'}
                        value={this.state.selected[0]}
                        onChange={(option) => this.onSelect(0, option)}
                        options={Array.apply(null, {
                            length: this.state.countRandomVariables
                        }).map((val, ind) => Object.assign({
                            value: ind,
                            label: numberToWord(ind+1),
                        }))}
                    />
                    <Select
                        name={'second-elem'}
                        removeSelected={true}
                        className={'two columns'}
                        value={this.state.selected[1]}
                        onChange={(option) => this.onSelect(1, option)}
                        options={Array.apply(null, {
                            length: this.state.countRandomVariables
                        }).map((val, ind) => Object.assign({
                            value: ind,
                            label: numberToWord(ind+1),
                        }))}
                    />
                </div>
                {if_then(
                    this.state.selected[0] &&
                    this.state.selected[1]
                    , () => (
                        <div className={'u-full-width'}>
                            {/*Checkboxes to choose graphic's model*/}
                            <div className={'row'}>
                                <label htmlFor={'select-plotter'}>Plot type:</label>
                                <Select
                                    name={'select-plotter'}
                                    removeSelected={true}
                                    value={this.state.plotType}
                                    onChange={(option) => {
                                        if (option == null) return;
                                        this.setState({ plotType: option });
                                    }}
                                    options={this.state.plotTypes.map(label => Object.assign({label}))}
                                />
                            </div>
                            <div className={'row'}>
                                {if_then(
                                    this.state.plotType &&
                                    this.state.plotType.label === 'surface',
                                    () => (
                                        <Plot data={[{
                                            type: 'surface',
                                            x: this.state.data.x,
                                            y: this.state.data.y,
                                            z: this.state.data.z,
                                        }]}
                                        />
                                ))}
                                {if_then(
                                    this.state.plotType &&
                                    this.state.plotType.label === 'isolines',
                                    () => (
                                        <div className={'row'}>
                                            <div className={'row'}>
                                                <label htmlFor={`${name(Input)}-${'countDots'}`}>
                                                    Count variables:
                                                </label>
                                                <Input
                                                    class={'two columns'}
                                                    onChange={(event) => this.onChangeGenSize(event.target.value)}
                                                    value={this.state.generated.size}
                                                />
                                            </div>
                                            <Plot
                                                data={[{
                                                    type: 'contour',
                                                    x: this.state.data.x,
                                                    y: this.state.data.y,
                                                    z: this.state.data.z,
                                                    contours: {
                                                        coloring: 'lines',
                                                    },
                                                }, {
                                                    type: 'scatter',
                                                    mode: 'markers',
                                                    x: this.state.generated.dots[this.state.selected[1].value],
                                                    y: this.state.generated.dots[this.state.selected[0].value],
                                                }]}
                                                layout={{
                                                    xaxis: {
                                                        // dtick: 0.25
                                                        // scaleratio: 1,
                                                        // domain: [-10, 10],
                                                        // showgrid: true,
                                                        // autotick: true,
                                                        // autorange: false,
                                                    },
                                                    yaxis: {
                                                        // dtick: 0.25
                                                        // scaleratio: 1,
                                                        // autorange: false,
                                                        // domain: [-10, 10],
                                                        // showgrid: true,
                                                        // autotick: true,
                                                    },
                                                    height: 700,
                                                    width: 700,
                                                }}
                                            />
                                            {if_then(this.state.generated.dots.length, () => (
                                                <div className={'raw'}>
                                                    <label htmlFor={`${name(InfinityLine)}-${'Computed'}`}>
                                                        Computed values:
                                                    </label>
                                                    {/*Mean variables*/}
                                                    <div className={'raw'}>
                                                        <label>Mean variables:</label>
                                                        <div>
                                                            {this.state.mean_t.map((val, ind) =>
                                                                (<Input
                                                                    class={'two columns'}
                                                                    key={ind}
                                                                    readOnly={true}
                                                                    value={val}
                                                                />)
                                                            )}
                                                        </div>
                                                    </div><br/><br/>

                                                    {/*Normalized correlation matrix*/}
                                                    <div className={'raw'}>
                                                        <label>Normalized correlation matrix:</label>
                                                        <div>
                                                            {this.state.r_t.map((row, rowInd) => {
                                                                return (
                                                                    <div className={'row'} key={rowInd}>
                                                                        {row.map((val, columnInd) => {
                                                                            return (
                                                                                <Input
                                                                                    style={{
                                                                                        marginBottom: 0,
                                                                                    }}
                                                                                    class={'two columns'}
                                                                                    key={rowInd + columnInd}
                                                                                    readOnly={true}
                                                                                    value={val}
                                                                                />
                                                                            )
                                                                        })}
                                                                    </div>
                                                                )
                                                            })}
                                                        </div>
                                                    </div>

                                                    {/*Dispersion vector*/}
                                                    <div className={'raw'}>
                                                        <label>Dispersion vector:</label>
                                                        <div className={`${InfinityLine} ${'dispersionVector'}`}>
                                                            {this.state.D_t.map((val, ind) =>
                                                                (<Input
                                                                    class={'two columns'}
                                                                    key={ind}
                                                                    readOnly={true}
                                                                    value={val}
                                                                />)
                                                            )}
                                                        </div>
                                                    </div>
                                                </div>
                                                ))}
                                        </div>
                                    )
                                )}
                            </div>
                        </div>
                ))}
            </div>
        )
    }
}

export default App;
