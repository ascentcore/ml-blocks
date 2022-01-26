import React, { useEffect, useState } from 'react';
import schema from '../custom-registry-schema.json';
import { SchemaForm } from '@ascentcore/react-schema-form';
import { TextField, Slider, Grid, Radio, RadioGroup, FormControlLabel, FormControl, FormLabel, Checkbox, InputLabel, Select, MenuItem } from '@mui/material';
import { useStyles } from './CustomRegistry.styles';

import addIcon from './add-icon.png';

import { MapContainer, TileLayer, Marker } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

import L from 'leaflet';
import { Box } from '@mui/system';

delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
    iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
    iconUrl: require('leaflet/dist/images/marker-icon.png'),
    shadowUrl: require('leaflet/dist/images/marker-shadow.png')
});

function MUIWrapper({ children }) {
    return <Grid container> <Grid item xs={2}>{children}</Grid></Grid>
}

function MUITextField({ property, value, onChange }) {
    const classes = useStyles();

    const handleChange = (event) => {
        onChange(event.target.value)
    }
    return (
        <TextField
            value={value || ''}
            onChange={handleChange}
            error={!!property.error}
            label={property.title}
            helperText={property.error ? property.error[0].keyword : ' '}
            required={property.isRequired}
            className={classes.input}
        />
    )
}

function MUIType({ property }) {
    const [value, setValue] = useState(property.enum[0]);
    const handleChange = (e) => {
        setValue(e.target.value);
    }
    return (
        <FormControl>
            <>{property.title}*</>
            <RadioGroup value={value} onChange={handleChange}>
                <FormControlLabel
                    control={<Radio />}
                    label={property.enum[0]}
                    value={property.enum[0]}
                />
                <FormControlLabel
                    control={<Radio />}
                    label={property.enum[1]}
                    value={property.enum[1]}
                />
                <FormControlLabel
                    control={<Radio />}
                    label={property.enum[2]}
                    value={property.enum[2]}
                />
                <FormControlLabel
                    control={<Radio />}
                    label={property.enum[3]}
                    value={property.enum[3]}
                />
            </RadioGroup>
        </FormControl>
    )
}

function MUICheckbox({ property }) {
    return (
        <>
            {property.title}
            <Checkbox />
        </>
    )
}

function MUINumberField({ property }) {
    const [value, setValue] = useState();
    const handleChange = (e) => {
        const re = property.pattern;
        if (e.target.value === '' || re.test(e.target.value)) {
            setValue(e.target.value)
        }
    }
    return (
        <>
            {property.title}
            <TextField
                value={value || 0}
                onChange={handleChange}
                helperText={property.error ? property.error[0].keyword : ' '}
                required={property.isRequired}
            />

        </>
    )
}

function MUIAddButton({ property, onChange }) {
    const classes = useStyles();
    return (
        < img
            className={classes.addButton}
            onClick={onChange}
            src={addIcon}
            alt='add icon'
        />
    )
}

function MUISelectElement({ property }) {
    const classes = useStyles();
    const [value, setValue] = React.useState('');

    const handleChange = (event) => {
        setValue(event.target.value);
    };
    return (
        <Grid container direction="row" className={classes.grid}>
            {property.title}
            <Select
                value={value}
                onChange={handleChange}
                className={classes.selector}
            >
                <MenuItem value={property.enum[0]}>{property.enum[0]}</MenuItem>
                <MenuItem value={property.enum[1]}>{property.enum[1]}</MenuItem>
            </Select>
        </Grid>
    )
}

function MUISlider({ property, value, onChange }) {
    const classes = useStyles();
    const handleChange = (event, newValue) => {
        onChange(newValue)
    }

    return (

        <Slider
            value={value !== undefined ? value : property.minimum ? property.minimum : 0}
            min={property.minimum ? property.minimum : 0}
            onChange={handleChange}
            valueLabelDisplay='auto'
            className={classes.slider}
        />
    )
}

function CustomLocation({ value, onChange }) {
    const classes = useStyles();

    const [coordinates, setCoordinates] = useState([46.753731, 23.605707])
    useEffect(() => {
        if (value && value.latitude && value.longitude) {
            setCoordinates([value.latitude, value.longitude])
        }
    }, [])

    useEffect(() => {
        if (value && value.latitude && value.longitude) {
            setCoordinates([value.latitude, value.longitude])
        }
    }, [value])

    const onMapClick = (event) => {
        onChange({ latitude: event.latlng.lat, longitude: event.latlng.lng })
    }

    return (
        <MapContainer center={coordinates} zoom={15} className={classes.map} onClick={onMapClick}>
            <TileLayer
                url='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
                attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            />
            <Marker position={coordinates}>
            </Marker>
        </MapContainer>

    )
}

export default function CustomRegistryExample() {
    function onSubmit(data, errors) {
        if (!errors || !errors.length) {
            console.log(data)
        }
    }

    const data = {
        firstName: 'test',
        age: 18
    }

    const customRegistry = {
        string: { component: MUITextField, wrapper: MUIWrapper },
        integer: { component: MUISlider, wrapper: MUIWrapper },
        enum: { component: MUIType, wrapper: MUIWrapper },
        addButton: { component: MUIAddButton, wrapper: MUIWrapper },
        boolean: { component: MUICheckbox, wrapper: MUIWrapper },
        //array: { component: MUINumberField, wrapper: MUIWrapper }
    }

    const exceptions = {
        keys: {
            writing: { component: MUISelectElement, wrapper: MUIWrapper },
            location: { component: CustomLocation, wrapper: MUIWrapper }
        }
    }

    return (
        <SchemaForm
            schema={schema}
            onSubmit={onSubmit}
            data={data}
            config={{ registry: customRegistry, exceptions: exceptions }}
        />
    )
}