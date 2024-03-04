import {
    Card,
} from "@material-tailwind/react";
import {
    PresentationChartBarIcon,
    UserCircleIcon,
    Cog6ToothIcon,
} from "@heroicons/react/24/solid";

import {Link} from 'react-router-dom';

export function DefaultSidebar() {
    return (
        <Card className="h-[calc(100vh-2rem)] w-full max-w-[12rem] m-4 shadow-xl shadow-blue-gray-900/5">
            <div
                className="relative flex flex-col bg-clip-border rounded-xl bg-white text-gray-700 h-[calc(100vh-2rem)] w-full max-w-[20rem] p-4 shadow-xl shadow-blue-gray-900/5">
                <nav className="flex flex-col gap-1 w-32 p-2 font-sans text-base font-normal text-gray-700">
                    <Link className="w-32" to="/">
                        <div role="button" tabIndex="0"
                             className="flex items-center w-full p-3 rounded-lg text-start leading-tight transition-all hover:bg-teal-50 hover:bg-opacity-80 active:bg-teal-50 active:bg-opacity-80 hover:text-green-700 active:text-green-700 outline-none">
                            <div className="grid place-items-center mr-4">
                                <PresentationChartBarIcon className="h-5 w-5"/>
                            </div>
                            Logs
                        </div>
                    </Link>

                    <Link className="w-32" to="/settings">
                        <div role="button" tabIndex="0"
                             className="flex items-center w-full p-3 rounded-lg text-start leading-tight transition-all hover:bg-teal-50 hover:bg-opacity-80 active:bg-teal-50 active:bg-opacity-80 hover:text-green-700 active:text-green-700 outline-none">
                            <div className="grid place-items-center mr-4">
                                <Cog6ToothIcon className="h-5 w-5"/>
                            </div>
                            Settings
                        </div>
                    </Link>

                    <Link className="w-32" to="/about">
                        <div role="button" tabIndex="0"
                             className="flex items-center w-full p-3 rounded-lg text-start leading-tight transition-all hover:bg-teal-50 hover:bg-opacity-80 active:bg-teal-50 active:bg-opacity-80 hover:text-green-700 active:text-green-700 outline-none">
                            <div className="grid place-items-center mr-4">
                                <UserCircleIcon className="h-5 w-5"/>
                            </div>
                            About
                        </div>
                    </Link>
                </nav>
            </div>
        </Card>
    );
}