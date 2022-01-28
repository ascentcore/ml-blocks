import React from 'react';
import { Route, Switch } from 'react-router-dom';
import HomeScreen from './screens/HomeScreen';

function Routes() {
    return (
        <Switch>
            <Route exact path="/" component={HomeScreen} />
            <Route path="/upload" />
        </Switch>
    )
}

export default Routes;