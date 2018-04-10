import React, { Component } from 'react';
import { BrowserRouter, Route } from 'react-router-dom';

import App from '../App';

export default class LocalRouter extends Component {
    render() {
        return (
            <div>
                <BrowserRouter>
                    <Route exact path="/" component={App} />
                </BrowserRouter>
            </div>
        )
    }
}