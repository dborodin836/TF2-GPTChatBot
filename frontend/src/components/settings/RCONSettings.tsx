import {Card, Input, Typography} from "@material-tailwind/react";
import React from "react";
import * as PropTypes from "prop-types";
import {Settings} from "./SettingsType";

export function RCONSettings(props: {
    settings: Settings | null;
    onChangeInput: React.ChangeEventHandler<HTMLInputElement> | undefined;
}) {
    return <Card className="p-6 w-full">
        <Typography className="mb-3" variant="h2">RCON</Typography>
        <hr className="mb-3"/>
        <div className="flex">
            <div className="mb-3 w-[100%]">
                <label
                    className="mb-2 inline-block text-neutral-500 dark:text-neutral-400"
                >RCON Host</label>
                <div className="min-w-[100%]">
                    <Input
                        className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                        labelProps={{
                            className: "hidden",
                        }}
                        containerProps={{className: "min-w-[100px]"}}
                        value={props.settings ? props.settings.RCON_HOST : ""}
                        name="RCON_HOST"
                        onChange={props.onChangeInput}
                    />
                </div>
            </div>

            <div className="mb-3 ml-3 w-[100%]">
                <label
                    className="mb-2 inline-block text-neutral-500 dark:text-neutral-400"
                >RCON Port</label>
                <div className="min-w-[100%]">
                    <Input
                        className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                        labelProps={{
                            className: "hidden",
                        }}
                        containerProps={{className: "min-w-[100px]"}}
                        value={props.settings ? props.settings.RCON_PORT : ""}
                        name="RCON_PORT"
                        onChange={props.onChangeInput}
                    />
                </div>
            </div>
        </div>


        <div className="mb-3">
            <label
                className="mb-2 inline-block text-neutral-500 dark:text-neutral-400"
            >RCON Password</label>
            <div className="min-w-[100%]">
                <Input
                    className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                    labelProps={{
                        className: "hidden",
                    }}
                    containerProps={{className: "min-w-[100px]"}}
                    value={props.settings ? props.settings.RCON_PASSWORD : ""}
                    name="RCON_PASSWORD"
                    onChange={props.onChangeInput}
                />
            </div>
        </div>
    </Card>;
}

RCONSettings.propTypes = {
    settings: PropTypes.any,
    onChangeInput: PropTypes.func
};