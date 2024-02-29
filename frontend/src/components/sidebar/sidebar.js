import {
    Card,
    List,
    ListItem,
    ListItemPrefix,
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
            <List className="w-32">
                <Link className="w-32" to="/">
                    <ListItem className="w-40 h-12">
                        <ListItemPrefix>
                            <PresentationChartBarIcon className="h-5 w-5"/>
                        </ListItemPrefix>
                        Logs
                    </ListItem>
                </Link>

                <Link className="w-32" to="/settings">
                    <ListItem className="w-40 h-12">
                        <ListItemPrefix>
                            <Cog6ToothIcon className="h-5 w-5"/>
                        </ListItemPrefix>
                        Settings
                    </ListItem>
                </Link>

                <Link className="w-32" to="/about">
                    <ListItem className="w-40 h-12">
                        <ListItemPrefix>
                            <UserCircleIcon className="h-5 w-5"/>
                        </ListItemPrefix>
                        About
                    </ListItem>
                </Link>
            </List>
        </Card>
    );
}