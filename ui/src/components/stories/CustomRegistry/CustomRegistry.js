import React from 'react';
import schema from '../custom-registry-schema.json';
import { SchemaForm } from '@ascentcore/react-schema-form';
import { TextField, Slider } from '@mui/material';

import addIcon from './add-icon.png';

function CustomWrapper({ children }) {
    return <div className='column col-12'>{children}</div>
}

function CustomTextField({ property, value, onChange }) {
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
        />
    )
}

function CustomAddButton({ property, onChange }) {
    return (
        <img
            className={property.className}
            onClick={onChange}
            src={addIcon}
            style={{ height: '15px' }}
            alt='add icon'
        />
    )
}

function CustomNumericField({ property, value, onChange }) {
    const handleChange = (event, newValue) => {
        onChange(newValue)
    }

    return (
        <Slider
            value={value !== undefined ? value : property.minimum ? property.minimum : 0}
            min={property.minimum ? property.minimum : 0}
            onChange={handleChange}
            valueLabelDisplay='auto'
        />
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
        string: { component: CustomTextField, wrapper: CustomWrapper },
        integer: { component: CustomNumericField, wrapper: CustomWrapper },
        enum: { component: 'RadioElement' },
        addButton: { component: CustomAddButton, wrapper: CustomWrapper }
    }

    const exceptions = {
        keys: {
            writing: { component: 'SelectElement' }
            //location: { component: CustomLocation, wrapper: CustomWrapper }
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