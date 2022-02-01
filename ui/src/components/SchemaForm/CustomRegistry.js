import React from 'react';
import schema from './custom-registry-schema.json';
import { SchemaForm } from '@ascentcore/react-schema-form';
import MUIWrapper from './Components/MUIWrapper';
import { MUIAddButton } from './Components/MUIAddButton';
import { MUICheckbox } from './Components/MUICheckbox';
import { MUISelectElement } from './Components/MUIDropdown';
import { MUILocation } from './Components/Map';
import { MUITextField } from './Components/MUITextField';
import { MUIRadioButtons } from './Components/MUIRadioButtons';
import { MUISlider } from './Components/MUISlider';

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
        enum: { component: MUIRadioButtons, wrapper: MUIWrapper },
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