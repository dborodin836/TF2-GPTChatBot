import {Card, Input, Switch, Textarea, Typography} from "@material-tailwind/react";
import React from "react";
import * as PropTypes from "prop-types";
import {Settings} from "./SettingsType";

export function ChatSettings(props: {
    settings: Settings | null;
    onChangeInput: any;
    onChangeToggle: any;
}) {
    return <Card className="p-6 w-full">
        <Typography className="mb-3" variant="h2">Chat</Typography>
        <hr className="mb-3"/>
        <div className="flex">
            <div className="mb-3 w-[100%]">
                <label className="mb-2 inline-block text-neutral-500 dark:text-neutral-400">
                    Clear Chat Command
                </label>
                <div className="min-w-[100%]">
                    <Input
                        className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                        labelProps={{
                            className: "hidden",
                        }}
                        containerProps={{className: "min-w-[100px]"}}
                        value={props.settings ? props.settings.CLEAR_CHAT_COMMAND : ""}
                        name="CLEAR_CHAT_COMMAND"
                        onChange={props.onChangeInput}
                    />
                </div>
            </div>

            <div className="mb-3 ml-3 w-[100%]">
                <label
                    className="mb-2 inline-block text-neutral-500 dark:text-neutral-400"
                >Delay Between Messages</label>
                <div className="min-w-[100%]">
                    <Input
                        className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                        labelProps={{
                            className: "hidden",
                        }}
                        containerProps={{className: "min-w-[100px]"}}
                        value={props.settings ? props.settings.DELAY_BETWEEN_MESSAGES : ""}
                        name="DELAY_BETWEEN_MESSAGES"
                        onChange={props.onChangeInput}
                    />
                </div>
            </div>
        </div>

        <div className="flex">
            <div className="mb-3 w-[100%]">
                <label
                    className="mb-2 inline-block text-neutral-500 dark:text-neutral-400"
                >Soft Completion Limit</label>
                <div className="min-w-[100%]">
                    <Input
                        className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                        labelProps={{
                            className: "hidden",
                        }}
                        containerProps={{className: "min-w-[100px]"}}
                        value={props.settings ? props.settings.SOFT_COMPLETION_LIMIT : ""}
                        name="SOFT_COMPLETION_LIMIT"
                        onChange={props.onChangeInput}
                    />
                </div>
            </div>

            <div className="mb-3 ml-3 w-[100%]">
                <label className="mb-2 inline-block text-neutral-500 dark:text-neutral-400">
                    Hard Completion Limit
                </label>
                <div className="min-w-[100%]">
                    <Input
                        className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                        labelProps={{
                            className: "hidden",
                        }}
                        containerProps={{className: "min-w-[100px]"}}
                        value={props.settings ? props.settings.HARD_COMPLETION_LIMIT : ""}
                        name="HARD_COMPLETION_LIMIT"
                        onChange={props.onChangeInput}
                    />
                </div>
            </div>
        </div>

        <Typography className="mb-3 mt-2" variant="h4">Shortened Username Response</Typography>
        <hr className="mb-3"/>

        <div className="ml-1 mb-3">
            <Switch label="Enable Shortened Username Response"
                    checked={props.settings?.ENABLE_SHORTENED_USERNAMES_RESPONSE || false}
                    name="ENABLE_SHORTENED_USERNAMES_RESPONSE"
                    onChange={props.onChangeToggle}/>
        </div>

        <hr className="mb-3"/>

        <div className="flex">
            <div className="mb-3 w-[100%]">
                <label
                    className="mb-2 inline-block text-neutral-500 dark:text-neutral-400"
                >Shortened Username Format</label>
                <div className="min-w-[100%]">
                    <Input
                        className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                        labelProps={{
                            className: "hidden",
                        }}
                        containerProps={{className: "min-w-[100px]"}}
                        value={props.settings ? props.settings.SHORTENED_USERNAMES_FORMAT : ""}
                        name="SHORTENED_USERNAMES_FORMAT"
                        onChange={props.onChangeInput}
                    />
                </div>
            </div>

            <div className="mb-3 ml-3 w-[100%]">
                <label className="mb-2 inline-block text-neutral-500 dark:text-neutral-400">
                    Shortened Username Length
                </label>
                <div className="min-w-[100%]">
                    <Input
                        className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                        labelProps={{
                            className: "hidden",
                        }}
                        containerProps={{className: "min-w-[100px]"}}
                        value={props.settings ? props.settings.SHORTENED_USERNAME_LENGTH : ""}
                        name="SHORTENED_USERNAME_LENGTH"
                        onChange={props.onChangeInput}
                    />
                </div>
            </div>
        </div>

        <Typography className="mb-3 mt-2" variant="h4">Behaviour</Typography>
        <hr className="mb-3"/>

        <label className="mb-2 inline-block text-neutral-500 dark:text-neutral-400">
            User Prompt Suffix
        </label>
        <Textarea
            className="!border mb-3 !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
            size="lg"
            id="textarea_logs"
            labelProps={{
                className: "hidden",
            }}
            value={props.settings ? props.settings.CUSTOM_PROMPT : ""}
            name="CUSTOM_PROMPT"
            onChange={props.onChangeInput}
        />

        <label className="mb-2 inline-block text-neutral-500 dark:text-neutral-400">
            AI Greeting Message
        </label>
        <Textarea
            className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
            size="lg"
            id="textarea_logs"
            labelProps={{
                className: "hidden",
            }}
            value={props.settings ? props.settings.GREETING : ""}
            name="GREETING"
            onChange={props.onChangeInput}
        />
    </Card>;
}

ChatSettings.propTypes = {
    settings: PropTypes.any,
    onChangeInput: PropTypes.func,
    onChangeToggle: PropTypes.func
};