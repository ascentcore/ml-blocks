import React from 'react';
import schema from './upload-schema.json';
import { SchemaForm } from '@ascentcore/react-schema-form';
import { MUICheckbox } from './Components/Checkbox';
import MUIWrapper from './Components/Wrapper';
import { MUISubmit } from './Components/MUISubmit';
import { MUIChooseFile } from './Components/MUIChooseFile';

export default function Upload() {
    function onSubmit(data, errors) {
        if (!errors || !errors.length) {
            console.log(data)
        }
    }

    const append = {
        button: { component: MUISubmit, wrapper: MUIWrapper },
        boolean: { component: MUICheckbox, wrapper: MUIWrapper },
        file: { component: MUIChooseFile, wrapper: MUIWrapper }
    }

    return (
        <SchemaForm
            schema={schema}
            onSubmit={onSubmit}
            config={{ registry: append }}
        />
    )
}