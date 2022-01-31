import React from 'react';
import { Route, Switch } from 'react-router-dom';
import HomeScreen from './screens/HomeScreen';
import UploadScreen from './screens/UploadScreen';

function Routes() {
    return (
        <Switch>
            <Route exact path="/" component={HomeScreen} />
            <Route exact path="/upload" component={UploadScreen} />
        </Switch>
    )
}

export default Routes;