import {Card, Switch, Typography} from "@material-tailwind/react";
import React from "react";
import * as PropTypes from "prop-types";

export function MiscellaneousSettings(props) {
    return <Card className="p-6 w-full">
        <Typography className="mb-3" variant="h2">Miscellaneous</Typography>

        <hr className="mb-3"/>

        <div className="ml-1 mb-3">
            <Switch label="Disable Keyboard Bindings"
                    checked={props.settings?.DISABLE_KEYBOARD_BINDINGS || false}
                    name="DISABLE_KEYBOARD_BINDINGS"
                    onChange={props.onChangeToggle}/>
        </div>

        <hr className="mb-3"/>

        <div className="ml-1 mb-3">
            <Switch label="Fallback to username to check permissions"
                    checked={props.settings?.FALLBACK_TO_USERNAME || false}
                    name="FALLBACK_TO_USERNAME"
                    onChange={props.onChangeToggle}/>
        </div>

        <hr className="mb-3"/>
    </Card>;
}

MiscellaneousSettings.propTypes = {
    settings: PropTypes.any,
    onChangeToggle: PropTypes.func
};