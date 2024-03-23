import {Card, Switch, Typography} from "@material-tailwind/react";
import {ExclamationTriangleIcon} from "@heroicons/react/24/solid";
import React from "react";
import * as PropTypes from "prop-types";
import {Settings} from "./SettingsType";

export function ExperimentalSettings(props: {
    settings: Settings | null;
    onChangeToggle: React.ChangeEventHandler<HTMLInputElement> | undefined;
}) {
    return <Card className="p-6 w-full">
        <Typography className="mb-3" variant="h2">
                    <span className="flex items-center">
                      Experimental <ExclamationTriangleIcon
                        className="h-8 w-8 text-yellow-700 ml-2 inline-block align-middle"/>
                    </span>
        </Typography>

        <hr className="mb-3"/>

        <div className="ml-1 mb-3">
            <Switch label="Enable Confirmable Queue"
                    checked={props.settings?.CONFIRMABLE_QUEUE || false}
                    name="CONFIRMABLE_QUEUE"
                    onChange={props.onChangeToggle}/>
        </div>

        <hr className="mb-3"/>
    </Card>;
}

ExperimentalSettings.propTypes = {
    settings: PropTypes.any,
    onChangeToggle: PropTypes.func
};