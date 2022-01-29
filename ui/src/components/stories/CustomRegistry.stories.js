import React from "react";
import CustomRegistryExample from "../SchemaForm/CustomRegistry";

const ComponentStory = {
    title: 'CustomRegistryExample',
    component: CustomRegistryExample,
}
export default ComponentStory;

const Template = (args) => <CustomRegistryExample {...args} />
export const CustomRegistryState = Template.bind({});
