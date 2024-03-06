import {Card, Input, Radio, Switch, Typography} from "@material-tailwind/react";
import React, {useEffect, useState} from "react";

export function PageSettings() {

    const [settings, setSettings] = useState(null);

    useEffect(() => {
        // Function to fetch settings
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

        // Call fetchSettings
        fetchSettings();
    }, []);

    const toggleEnableStats = () => {
        setSettings({
            ...settings,
            ENABLE_STATS: !settings.ENABLE_STATS,
        });
    };

    const handleRTDModeChange = (mode) => {
        setSettings((prevSettings) => ({
            ...prevSettings,
            RTD_MODE: mode,
        }));
    };

    return (
        <div className="flex flex-1 max-h-[calc(100vh-2rem)] flex-col text-gray-700 w-full gap-6 p-4 overflow-y-scroll">
            <Card className="p-6">
                <Typography className="mb-3" variant="h2">Required Settings</Typography>
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
                        />
                    </div>
                </div>

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
                        />
                    </div>
                </div>
            </Card>

            <Card className="p-6">
                <Typography className="mb-3" variant="h2">RCON Settings</Typography>
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
                        />
                    </div>
                </div>
            </Card>

            <Card className="p-6">
                <Typography className="mb-3" variant="h2">Stats Settings</Typography>

                <hr className="mb-3"/>

                <div className="ml-1 mb-3">
                    <Switch label="Enable Stats Module"
                            checked={settings?.ENABLE_STATS || false}
                            onChange={toggleEnableStats}/>
                </div>

                <hr className="mb-3"/>

                <div className="mb-3 ml-3 w-[100%]">
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
                        />
                    </div>
                </div>
            </Card>

            <Card className="p-6">
                <Typography className="mb-3" variant="h2">RTD Settings</Typography>

                <hr className="mb-3"/>

                <Typography className="mb-3" variant="h4">RTD Mode</Typography>
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

            <Card className="p-6">
                <Typography className="mb-3" variant="h2">OpenAI Models & Commands</Typography>
                <hr className="mb-3"/>
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
                                />
                            </div>
                        </div>
                    </div>

                    <div className="flex">
                        <div className="mb-3 w-[100%]">
                            <label
                                className="mb-2 inline-block text-neutral-500 dark:text-neutral-400"
                            >Chat Command</label>
                            <div className="w-72 min-w-[100%]">
                                <Input
                                    className="!border !border-gray-300 bg-white text-gray-900 shadow-lg shadow-gray-900/5 ring-4 ring-transparent placeholder:text-gray-500 focus:!border-gray-900 focus:!border-t-gray-900 focus:ring-gray-900/10"
                                    labelProps={{
                                        className: "hidden",
                                    }}
                                    containerProps={{className: "min-w-[100px]"}}
                                    value={settings ? settings.CHATGPT_COMMAND : ''}
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
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </Card>


            <Card className="p-6">
                <Typography className="mb-3" variant="h2">TEMPLATE</Typography>
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
                        />
                    </div>
                </div>

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
                        />
                    </div>
                </div>
            </Card>
        </div>
    );
}