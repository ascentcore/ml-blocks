import React from 'react';
import schema from './custom-registry-schema.json';
import { SchemaForm } from '@ascentcore/react-schema-form';
import MUIWrapper from './Components/Wrapper';
import { MUIAddButton } from './Components/AddButton';
import { MUICheckbox } from './Components/Checkbox';
import { MUISelectElement } from './Components/Dropdown';
import { MUILocation } from './Components/Map';
import { MUITextField } from './Components/TextField';
import { MUIType } from './Components/RadioButtons';
import { MUISlider } from './Components/Slider';

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
        boolean: { component: MUICheckbox, wrapper: MUIWrapper }
    }

    const exceptions = {
        keys: {
            writing: { component: MUISelectElement, wrapper: MUIWrapper },
            location: { component: MUILocation, wrapper: MUIWrapper }
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