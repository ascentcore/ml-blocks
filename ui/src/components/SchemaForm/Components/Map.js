import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { useStyles } from './Style.styles';

delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
    iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
    iconUrl: require('leaflet/dist/images/marker-icon.png'),
    shadowUrl: require('leaflet/dist/images/marker-shadow.png')
});

export function MUILocation({ value, onChange }) {
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