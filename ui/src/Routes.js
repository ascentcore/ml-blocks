import React from 'react';
import { Route, Switch } from 'react-router-dom';
import HomeScreen from './screens/HomeScreen';
import UploadScreen from './screens/UploadScreen';
import DataScreen from './screens/DataScreen';

function Routes() {
    return (
        <Switch>
            <Route exact path="/" component={HomeScreen} />
            <Route exact path="/upload" component={UploadScreen} />
            <Route exact path="/data" component={DataScreen} />
        </Switch>
    )
}

export default Routes;