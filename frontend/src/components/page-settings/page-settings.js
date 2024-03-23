import {Card, Input, Radio, Switch, Textarea, Typography} from "@material-tailwind/react";
import React, {useEffect, useState} from "react";
import {
    ExclamationTriangleIcon
} from "@heroicons/react/24/solid";
import {
    ArrowPathIcon,
    CheckIcon,
    XMarkIcon
} from "@heroicons/react/16/solid";

export function PageSettings() {

    const [settings, setSettings] = useState(null);

    const fetchSettings = async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/settings');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            setSettings(data);
            console.log(data);
        } catch (error) {
            console.error("Failed to fetch settings:", error);
        }
    };

    const fetchDefaultSettings = async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/settings/default');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            setSettings(data);
            console.log(data);
        } catch (error) {
            console.error("Failed to fetch default settings:", error);
        }
    };

    useEffect(() => {
        fetchSettings();
    }, []);

    const discardChanges = () => {
        fetchSettings();
    }

    const submitSettings = async () => {
        // Ensure there are settings to submit
        if (!settings) {
            console.log('No settings to submit');
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:8000/settings', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(settings),
            });

            if (!response.ok) {
                throw new Error(`Error: ${response.status}`);
            }

            const result = await response.json();
            console.log('Successfully submitted settings:', result);
        } catch (error) {
            console.error('Failed to submit settings:', error);
        }
    }

    const toggleEnableStats = () => {
        setSettings({
            ...settings,
            ENABLE_STATS_LOGS: !settings.ENABLE_STATS_LOGS,
        });
    };

    const toggleConfirmableQueue = () => {
        setSettings({
            ...settings,
            CONFIRMABLE_QUEUE: !settings.CONFIRMABLE_QUEUE,
        });
    };

    const toggleKeyboardBindings = () => {
        setSettings({
            ...settings,
            DISABLE_KEYBOARD_BINDINGS: !settings.DISABLE_KEYBOARD_BINDINGS,
        });
    }

    const toggleUsernamePermissions = () => {
        setSettings({
            ...settings,
            FALLBACK_TO_USERNAME: !settings.FALLBACK_TO_USERNAME,
        });
    }

    const toggleOpenAIModeration = () => {
        setSettings({
            ...settings,
            TOS_VIOLATION: !settings.TOS_VIOLATION,
        });
    }

    const toggleOpenAICommands = () => {
        setSettings({
            ...settings,
            ENABLE_OPENAI_COMMANDS: !settings.ENABLE_OPENAI_COMMANDS,
        });
    }

    const toggleShortenedUsernameResponse = () => {
        setSettings({
            ...settings,
            ENABLE_SHORTENED_USERNAMES_RESPONSE: !settings.ENABLE_SHORTENED_USERNAMES_RESPONSE,
        });
    }

    const toggleCustomModel = () => {
        setSettings({
            ...settings,
            ENABLE_CUSTOM_MODEL: !settings.ENABLE_CUSTOM_MODEL,
        });
    }

    const toggleSoftLimitForCustomModel = () => {
        setSettings({
            ...settings,
            ENABLE_SOFT_LIMIT_FOR_CUSTOM_MODEL: !settings.ENABLE_SOFT_LIMIT_FOR_CUSTOM_MODEL,
        });
    }

    const handleRTDModeChange = (mode) => {
        setSettings((prevSettings) => ({
            ...prevSettings,
            RTD_MODE: mode,
        }));
    };

    const handleInputChange = (e) => {
        const {name, value} = e.target;
        setSettings(prevSettings => ({
            ...prevSettings,
            [name]: value,
        }));
    };


    return (
        <>
            <Card className="flex border rounded-none shadow-none flex-row p-4 gap-6">
                <div role="button" onClick={submitSettings} tabIndex="0"
                     className="flex items-center w-51 hover:border-green-500 border-2 p-3 rounded-lg text-start leading-tight transition-all hover:bg-teal-50 hover:bg-opacity-80 active:bg-teal-50 active:bg-opacity-80 hover:text-green-700 active:text-green-700 outline-none">
                    <div className="grid place-items-center mr-4">
                        <CheckIcon className="h-5 w-5"/>
                    </div>
                    Save Changes
                </div>

                <div role="button" onClick={discardChanges} tabIndex="0"
                     className="flex items-center w-51 hover:border-red-500 border-2 p-3 rounded-lg text-start leading-tight transition-all hover:bg-red-50 hover:bg-opacity-80 active:bg-red-50 active:bg-opacity-80 hover:text-red-900 active:text-red-900 outline-none">
                    <div className="grid place-items-center mr-4">
                        <XMarkIcon className="h-5 w-5"/>
                    </div>
                    Discard Changes
                </div>

                <div role="button" onClick={fetchDefaultSettings} tabIndex="0"
                     className="flex items-center w-51 hover:border-blue-500 border-2 p-3 rounded-lg text-start leading-tight transition-all hover:bg-blue-50 hover:bg-opacity-80 active:bg-blue-50 active:bg-opacity-80 hover:text-light-blue-900 active:text-light-blue-900 outline-none">
                    <div className="grid place-items-center mr-4">
                        <ArrowPathIcon className="h-5 w-5"/>
                    </div>
                    Restore Defaults
                </div>
            </Card>

            <div
                className="flex flex-1 max-h-[calc(100vh-7rem)] flex-col text-gray-700 w-full gap-6 p-4 overflow-y-scroll">
                {/* Required */}
                <Card className="p-6 mt-15">
                    <Typography className="mb-3" variant="h2">
                    <span className="flex items-center">
                          Required Settings <ExclamationTriangleIcon
                        className="h-8 w-8 text-red-500 ml-2 inline-block align-middle"/>
                    </span></Typography>
                    <hr className="mb-3"/>
                    <div className="mb-3">
                        <label
                            className="mb-2 inline-block text-neutral-500 dark:text-neutral-400"
                        >console.log file location</label>
                        <div className="w-72 min-w-[100%]">
                            <Input
                                className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                                labelProps={{
                                    className: "hidden",
                                }}
                                containerProps={{className: "min-w-[100px]"}}
                                value={settings ? settings.TF2_LOGFILE_PATH : ''}
                                name="TF2_LOGFILE_PATH"
                                onChange={handleInputChange}
                            />
                        </div>
                    </div>
                </Card>

                {/* RCON */}
                <Card className="p-6">
                    <Typography className="mb-3" variant="h2">RCON</Typography>
                    <hr className="mb-3"/>
                    <div className="flex">
                        <div className="mb-3 w-[100%]">
                            <label
                                className="mb-2 inline-block text-neutral-500 dark:text-neutral-400"
                            >RCON Host</label>
                            <div className="w-72 min-w-[100%]">
                                <Input
                                    className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                                    labelProps={{
                                        className: "hidden",
                                    }}
                                    containerProps={{className: "min-w-[100px]"}}
                                    value={settings ? settings.RCON_HOST : ''}
                                    name="RCON_HOST"
                                    onChange={handleInputChange}
                                />
                            </div>
                        </div>

                        <div className="mb-3 ml-3 w-[100%]">
                            <label
                                className="mb-2 inline-block text-neutral-500 dark:text-neutral-400"
                            >RCON Port</label>
                            <div className="w-72 min-w-[100%]">
                                <Input
                                    className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                                    labelProps={{
                                        className: "hidden",
                                    }}
                                    containerProps={{className: "min-w-[100px]"}}
                                    value={settings ? settings.RCON_PORT : ''}
                                    name="RCON_PORT"
                                    onChange={handleInputChange}
                                />
                            </div>
                        </div>
                    </div>


                    <div className="mb-3">
                        <label
                            className="mb-2 inline-block text-neutral-500 dark:text-neutral-400"
                        >RCON Password</label>
                        <div className="w-72 min-w-[100%]">
                            <Input
                                className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                                labelProps={{
                                    className: "hidden",
                                }}
                                containerProps={{className: "min-w-[100px]"}}
                                value={settings ? settings.RCON_PASSWORD : ''}
                                name="RCON_PASSWORD"
                                onChange={handleInputChange}
                            />
                        </div>
                    </div>
                </Card>

                {/* OpenAI Settings*/}
                <Card className="p-6">
                    <Typography className="mb-3" variant="h2">OpenAI</Typography>
                    <hr className="mb-3"/>

                    <div className="ml-1 mb-3">
                        <Switch label="Enable OpenAI Commands"
                                checked={settings?.ENABLE_OPENAI_COMMANDS || false}
                                onChange={toggleOpenAICommands}/>
                    </div>

                    <hr className="mb-3"/>

                    <div className="ml-1 mb-3">
                        <Switch label="Enable Message Moderation"
                                checked={!settings?.TOS_VIOLATION || true}
                                onChange={toggleOpenAIModeration}/>
                    </div>

                    <hr className="mb-3"/>

                    <div className="mb-3">
                        <label
                            className="mb-2 inline-block text-neutral-500 dark:text-neutral-400"
                        >OpenAI API Key</label>
                        <div className="w-72 min-w-[100%]">
                            <Input
                                className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                                labelProps={{
                                    className: "hidden",
                                }}
                                containerProps={{className: "min-w-[100px]"}}
                                value={settings ? settings.OPENAI_API_KEY : ''}
                                name="OPENAI_API_KEY"
                                onChange={handleInputChange}
                            />
                        </div>
                    </div>

                    <div className="mb-3">
                        <div className="flex">
                            <div className="mb-3 w-[100%]">
                                <label
                                    className="mb-2 inline-block text-neutral-500 dark:text-neutral-400"
                                >GPT3 Model Command</label>
                                <div className="w-72 min-w-[100%]">
                                    <Input
                                        className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                                        labelProps={{
                                            className: "hidden",
                                        }}
                                        containerProps={{className: "min-w-[100px]"}}
                                        value={settings ? settings.GPT_COMMAND : ''}
                                        name="GPT_COMMAND"
                                        onChange={handleInputChange}
                                    />
                                </div>
                            </div>

                            <div className="mb-3 ml-3 w-[100%]">
                                <label
                                    className="mb-2 inline-block text-neutral-500 dark:text-neutral-400"
                                >GPT3 Model</label>
                                <div className="w-72 min-w-[100%]">
                                    <Input
                                        className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                                        labelProps={{
                                            className: "hidden",
                                        }}
                                        containerProps={{className: "min-w-[100px]"}}
                                        value={settings ? settings.GPT3_MODEL : ''}
                                        name="GPT3_MODEL"
                                        onChange={handleInputChange}
                                    />
                                </div>
                            </div>
                        </div>

                        <div className="flex">
                            <div className="mb-3 w-[100%]">
                                <label
                                    className="mb-2 inline-block text-neutral-500 dark:text-neutral-400"
                                >GPT4 Model Command</label>
                                <div className="w-72 min-w-[100%]">
                                    <Input
                                        className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                                        labelProps={{
                                            className: "hidden",
                                        }}
                                        containerProps={{className: "min-w-[100px]"}}
                                        value={settings ? settings.GPT4_COMMAND : ''}
                                        name="GPT4_COMMAND"
                                        onChange={handleInputChange}
                                    />
                                </div>
                            </div>

                            <div className="mb-3 ml-3 w-[100%]">
                                <label
                                    className="mb-2 inline-block text-neutral-500 dark:text-neutral-400"
                                >GPT4 Model</label>
                                <div className="w-72 min-w-[100%]">
                                    <Input
                                        className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                                        labelProps={{
                                            className: "hidden",
                                        }}
                                        containerProps={{className: "min-w-[100px]"}}
                                        value={settings ? settings.GPT4_MODEL : ''}
                                        name="GPT4_MODEL"
                                        onChange={handleInputChange}
                                    />
                                </div>
                            </div>
                        </div>

                        <div className="flex">
                            <div className="mb-3 w-[100%]">
                                <label
                                    className="mb-2 inline-block text-neutral-500 dark:text-neutral-400"
                                >GPT4 Legacy Model Command</label>
                                <div className="w-72 min-w-[100%]">
                                    <Input
                                        className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                                        labelProps={{
                                            className: "hidden",
                                        }}
                                        containerProps={{className: "min-w-[100px]"}}
                                        value={settings ? settings.GPT4_LEGACY_COMMAND : ''}
                                        name="GPT4_LEGACY_COMMAND"
                                        onChange={handleInputChange}
                                    />
                                </div>
                            </div>

                            <div className="mb-3 ml-3 w-[100%]">
                                <label
                                    className="mb-2 inline-block text-neutral-500 dark:text-neutral-400"
                                >GPT4 Legacy Model</label>
                                <div className="w-72 min-w-[100%]">
                                    <Input
                                        className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                                        labelProps={{
                                            className: "hidden",
                                        }}
                                        containerProps={{className: "min-w-[100px]"}}
                                        value={settings ? settings.GPT4L_MODEL : ''}
                                        name="GPT4L_MODEL"
                                        onChange={handleInputChange}
                                    />
                                </div>
                            </div>
                        </div>

                        <div className="flex">
                            <div className="mb-3 w-[100%]">
                                <label
                                    className="mb-2 inline-block text-neutral-500 dark:text-neutral-400"
                                >Global Chat Command</label>
                                <div className="w-72 min-w-[100%]">
                                    <Input
                                        className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                                        labelProps={{
                                            className: "hidden",
                                        }}
                                        containerProps={{className: "min-w-[100px]"}}
                                        value={settings ? settings.GLOBAL_CHAT_COMMAND : ''}
                                        name="GLOBAL_CHAT_COMMAND"
                                        onChange={handleInputChange}
                                    />
                                </div>
                            </div>

                            <div className="mb-3 ml-3 w-[100%]">
                                <label
                                    className="mb-2 inline-block text-neutral-500 dark:text-neutral-400"
                                >Private Chat Command</label>
                                <div className="w-72 min-w-[100%]">
                                    <Input
                                        className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                                        labelProps={{
                                            className: "hidden",
                                        }}
                                        containerProps={{className: "min-w-[100px]"}}
                                        value={settings ? settings.CHATGPT_COMMAND : ''}
                                        name="CHATGPT_COMMAND"
                                        onChange={handleInputChange}
                                    />
                                </div>
                            </div>

                            <div className="mb-3 ml-3 w-[100%]">
                                <label
                                    className="mb-2 inline-block text-neutral-500 dark:text-neutral-400"
                                >Chat Model</label>
                                <div className="w-72 min-w-[100%]">
                                    <Input
                                        className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                                        labelProps={{
                                            className: "hidden",
                                        }}
                                        containerProps={{className: "min-w-[100px]"}}
                                        value={settings ? settings.GPT3_CHAT_MODEL : ''}
                                        name="GPT3_CHAT_MODEL"
                                        onChange={handleInputChange}
                                    />
                                </div>
                            </div>
                        </div>
                    </div>
                </Card>

                {/* Chat */}
                <Card className="p-6">
                    <Typography className="mb-3" variant="h2">Chat</Typography>
                    <hr className="mb-3"/>
                    <div className="flex">
                        <div className="mb-3 w-[100%]">
                            <label className="mb-2 inline-block text-neutral-500 dark:text-neutral-400">
                                Clear Chat Command
                            </label>
                            <div className="w-72 min-w-[100%]">
                                <Input
                                    className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                                    labelProps={{
                                        className: "hidden",
                                    }}
                                    containerProps={{className: "min-w-[100px]"}}
                                    value={settings ? settings.CLEAR_CHAT_COMMAND : ''}
                                    name="CLEAR_CHAT_COMMAND"
                                    onChange={handleInputChange}
                                />
                            </div>
                        </div>

                        <div className="mb-3 ml-3 w-[100%]">
                            <label
                                className="mb-2 inline-block text-neutral-500 dark:text-neutral-400"
                            >Delay Between Messages</label>
                            <div className="w-72 min-w-[100%]">
                                <Input
                                    className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                                    labelProps={{
                                        className: "hidden",
                                    }}
                                    containerProps={{className: "min-w-[100px]"}}
                                    value={settings ? settings.DELAY_BETWEEN_MESSAGES : ''}
                                    name="DELAY_BETWEEN_MESSAGES"
                                    onChange={handleInputChange}
                                />
                            </div>
                        </div>
                    </div>

                    <div className="flex">
                        <div className="mb-3 w-[100%]">
                            <label
                                className="mb-2 inline-block text-neutral-500 dark:text-neutral-400"
                            >Soft Completion Limit</label>
                            <div className="w-72 min-w-[100%]">
                                <Input
                                    className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                                    labelProps={{
                                        className: "hidden",
                                    }}
                                    containerProps={{className: "min-w-[100px]"}}
                                    value={settings ? settings.SOFT_COMPLETION_LIMIT : ''}
                                    name="SOFT_COMPLETION_LIMIT"
                                    onChange={handleInputChange}
                                />
                            </div>
                        </div>

                        <div className="mb-3 ml-3 w-[100%]">
                            <label className="mb-2 inline-block text-neutral-500 dark:text-neutral-400">
                                Hard Completion Limit
                            </label>
                            <div className="w-72 min-w-[100%]">
                                <Input
                                    className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                                    labelProps={{
                                        className: "hidden",
                                    }}
                                    containerProps={{className: "min-w-[100px]"}}
                                    value={settings ? settings.HARD_COMPLETION_LIMIT : ''}
                                    name="HARD_COMPLETION_LIMIT"
                                    onChange={handleInputChange}
                                />
                            </div>
                        </div>
                    </div>

                    <Typography className="mb-3 mt-2" variant="h4">Shortened Username Response</Typography>
                    <hr className="mb-3"/>

                    <div className="ml-1 mb-3">
                        <Switch label="Enable Shortened Username Response"
                                checked={settings?.ENABLE_SHORTENED_USERNAMES_RESPONSE || false}
                                onChange={toggleShortenedUsernameResponse}/>
                    </div>

                    <hr className="mb-3"/>

                    <div className="flex">
                        <div className="mb-3 w-[100%]">
                            <label
                                className="mb-2 inline-block text-neutral-500 dark:text-neutral-400"
                            >Shortened Username Format</label>
                            <div className="w-72 min-w-[100%]">
                                <Input
                                    className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                                    labelProps={{
                                        className: "hidden",
                                    }}
                                    containerProps={{className: "min-w-[100px]"}}
                                    value={settings ? settings.SHORTENED_USERNAMES_FORMAT : ''}
                                    name="SHORTENED_USERNAMES_FORMAT"
                                    onChange={handleInputChange}
                                />
                            </div>
                        </div>

                        <div className="mb-3 ml-3 w-[100%]">
                            <label className="mb-2 inline-block text-neutral-500 dark:text-neutral-400">
                                Shortened Username Length
                            </label>
                            <div className="w-72 min-w-[100%]">
                                <Input
                                    className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                                    labelProps={{
                                        className: "hidden",
                                    }}
                                    containerProps={{className: "min-w-[100px]"}}
                                    value={settings ? settings.SHORTENED_USERNAME_LENGTH : ''}
                                    name="SHORTENED_USERNAME_LENGTH"
                                    onChange={handleInputChange}
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
                        value={settings ? settings.CUSTOM_PROMPT : ''}
                        name="CUSTOM_PROMPT"
                        onChange={handleInputChange}
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
                        value={settings ? settings.GREETING : ''}
                        name="GREETING"
                        onChange={handleInputChange}
                    />
                </Card>

                {/* Textgen Webui */}
                <Card className="p-6">
                    <Typography className="mb-3" variant="h2">Text Generation WebUI</Typography>
                    <hr className="mb-3"/>

                    <div className="ml-1 mb-3">
                        <Switch label="Enable Text Generation WebUI Integration"
                                checked={settings?.ENABLE_CUSTOM_MODEL || false}
                                onChange={toggleCustomModel}/>
                    </div>
                    <hr className="mb-3"/>

                    <div className="ml-1 mb-3">
                        <Switch label="Enable Soft Completion Limit For Custom Model"
                                checked={settings?.ENABLE_SOFT_LIMIT_FOR_CUSTOM_MODEL || false}
                                onChange={toggleSoftLimitForCustomModel}/>
                    </div>
                    <hr className="mb-3"/>

                    <div className="flex">
                        <div className="mb-3 w-[100%]">
                            <label className="mb-2 inline-block text-neutral-500 dark:text-neutral-400">
                                Custom Model Command
                            </label>
                            <div className="w-72 min-w-[100%]">
                                <Input
                                    className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                                    labelProps={{
                                        className: "hidden",
                                    }}
                                    containerProps={{className: "min-w-[100px]"}}
                                    value={settings ? settings.CUSTOM_MODEL_COMMAND : ''}
                                    name="CUSTOM_MODEL_COMMAND"
                                    onChange={handleInputChange}
                                />
                            </div>
                        </div>

                        <div className="mb-3 ml-3 w-[100%]">
                            <label
                                className="mb-2 inline-block text-neutral-500 dark:text-neutral-400"
                            >Private Chat Command</label>
                            <div className="w-72 min-w-[100%]">
                                <Input
                                    className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                                    labelProps={{
                                        className: "hidden",
                                    }}
                                    containerProps={{className: "min-w-[100px]"}}
                                    value={settings ? settings.CUSTOM_MODEL_CHAT_COMMAND : ''}
                                    name="CUSTOM_MODEL_CHAT_COMMAND"
                                    onChange={handleInputChange}
                                />
                            </div>
                        </div>

                        <div className="mb-3 ml-3 w-[100%]">
                            <label
                                className="mb-2 inline-block text-neutral-500 dark:text-neutral-400"
                            >Global Chat Command</label>
                            <div className="w-72 min-w-[100%]">
                                <Input
                                    className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                                    labelProps={{
                                        className: "hidden",
                                    }}
                                    containerProps={{className: "min-w-[100px]"}}
                                    value={settings ? settings.GLOBAL_CUSTOM_CHAT_COMMAND : ''}
                                    name="GLOBAL_CUSTOM_CHAT_COMMAND"
                                    onChange={handleInputChange}
                                />
                            </div>
                        </div>
                    </div>

                    <div className="mb-3">
                        <label
                            className="mb-2 inline-block text-neutral-500 dark:text-neutral-400"
                        >Custom Model Host</label>
                        <div className="w-72 min-w-[100%]">
                            <Input
                                className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                                labelProps={{
                                    className: "hidden",
                                }}
                                containerProps={{className: "min-w-[100px]"}}
                                value={settings ? settings.CUSTOM_MODEL_HOST : ''}
                                name="CUSTOM_MODEL_HOST"
                                onChange={handleInputChange}
                            />
                        </div>
                    </div>

                    <label className="mb-2 inline-block text-neutral-500 dark:text-neutral-400">
                        Cutom Model Settings
                    </label>
                    <Textarea
                        className="!border mb-3 !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                        size="lg"
                        id="textarea_logs"
                        labelProps={{
                            className: "hidden",
                        }}
                        value={settings ? settings.CUSTOM_MODEL_SETTINGS : ''}
                        name="CUSTOM_MODEL_SETTINGS"
                        onChange={handleInputChange}
                    />
                </Card>

                {/* Stats */}
                <Card className="p-6">
                    <Typography className="mb-3" variant="h2">Statistics</Typography>

                    <hr className="mb-3"/>

                    <div className="ml-1 mb-3">
                        <Switch label="Enable Statistics Module"
                                checked={settings?.ENABLE_STATS_LOGS || false}
                                onChange={toggleEnableStats}/>
                    </div>

                    <hr className="mb-3"/>

                    <div className="mb-3 w-[100%]">
                        <label
                            className="mb-2 inline-block text-neutral-500 dark:text-neutral-400"
                        >Steam WebAPI Key</label>
                        <div className="w-72 min-w-[100%]">
                            <Input
                                className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                                labelProps={{
                                    className: "hidden",
                                }}
                                containerProps={{className: "min-w-[100px]"}}
                                value={settings ? settings.STEAM_WEBAPI_KEY : ''}
                                name="STEAM_WEBAPI_KEY"
                                onChange={handleInputChange}
                            />
                        </div>
                    </div>
                </Card>

                {/* RTD */}
                <Card className="p-6">
                    <Typography className="mb-3" variant="h2">RTD (Roll The Dice)</Typography>

                    <hr className="mb-3"/>

                    <label className="mb-2 inline-block text-neutral-500 dark:text-neutral-400">
                        RTD Mode
                    </label>
                    <div className="w-[100%]">
                        <div className="flex gap-8">
                            <Radio
                                name="description"
                                label={
                                    <div>
                                        <Typography color="blue-gray" className="font-medium">
                                            Disabled
                                        </Typography>
                                        <Typography variant="small" color="gray" className="font-normal">
                                            Disable module functionality.
                                        </Typography>
                                    </div>
                                }
                                checked={settings?.RTD_MODE === 0 || false}
                                onChange={() => {
                                    handleRTDModeChange(0)
                                }}
                                containerProps={{
                                    className: "-mt-5",
                                }}
                            />
                            <Radio
                                name="description"
                                label={
                                    <div>
                                        <Typography color="blue-gray" className="font-medium">
                                            RickRoll
                                        </Typography>
                                        <Typography variant="small" color="gray" className="font-normal">
                                            Sends the RickRoll link (<a target="_blank" rel="noreferrer"
                                                                        className="font-medium text-green-500 dark:text-green-blue-600 hover:underline"
                                                                        href="https://youtu.be/dQw4w9WgXcQ">youtu.be/dQw4w9WgXcQ</a>).
                                        </Typography>
                                    </div>
                                }
                                checked={settings?.RTD_MODE === 1 || false}
                                onChange={() => {
                                    handleRTDModeChange(1)
                                }}
                                containerProps={{
                                    className: "-mt-5",
                                }}
                            />
                            <Radio
                                name="description"
                                label={
                                    <div>
                                        <Typography color="blue-gray" className="font-medium">
                                            Random YouTube Meme
                                        </Typography>
                                        <Typography variant="small" color="gray" className="font-normal">
                                            Sends a random link from vids.txt file.
                                        </Typography>
                                    </div>
                                }
                                checked={settings?.RTD_MODE === 2 || false}
                                onChange={() => {
                                    handleRTDModeChange(2)
                                }}
                                containerProps={{
                                    className: "-mt-5",
                                }}
                            />
                        </div>
                    </div>
                </Card>

                {/* Miscellaneous */}
                <Card className="p-6">
                    <Typography className="mb-3" variant="h2">Miscellaneous</Typography>

                    <hr className="mb-3"/>

                    <div className="ml-1 mb-3">
                        <Switch label="Disable Keyboard Bindings"
                                checked={settings?.DISABLE_KEYBOARD_BINDINGS || false}
                                onChange={toggleKeyboardBindings}/>
                    </div>

                    <hr className="mb-3"/>

                    <div className="ml-1 mb-3">
                        <Switch label="Fallback to username to check permissions"
                                checked={settings?.FALLBACK_TO_USERNAME || false}
                                onChange={toggleUsernamePermissions}/>
                    </div>

                    <hr className="mb-3"/>
                </Card>

                {/* Experimental */}
                <Card className="p-6">
                    <Typography className="mb-3" variant="h2">
                    <span className="flex items-center">
                      Experimental <ExclamationTriangleIcon
                        className="h-8 w-8 text-yellow-700 ml-2 inline-block align-middle"/>
                    </span>
                    </Typography>

                    <hr className="mb-3"/>

                    <div className="ml-1 mb-3">
                        <Switch label="Enable Confirmable Queue"
                                checked={settings?.CONFIRMABLE_QUEUE || false}
                                onChange={toggleConfirmableQueue}/>
                    </div>

                    <hr className="mb-3"/>
                </Card>

            </div>
        </>
    );
}