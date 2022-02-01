import React from "react";
import Upload from "../SchemaForm/Upload";

const ComponentStory = {
    title: 'Upload',
    component: Upload,
}
export default ComponentStory;

const Template = (args) => <Upload {...args} />
export const UploadState = Template.bind({});
