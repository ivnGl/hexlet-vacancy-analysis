import { InertiaProgress } from '@inertiajs/progress';
import { createInertiaApp } from "@inertiajs/react";
import { MantineProvider } from '@mantine/core';
import '@mantine/core/styles.css';
import axios from 'axios';
import React from 'react';
import { createRoot } from "react-dom/client";
import "vite/modulepreload-polyfill";
import { themeRed } from './theme';


document.addEventListener('DOMContentLoaded', () => {

    const csrfToken = document.querySelector('meta[name=csrf-token]')?.getAttribute('content');
    axios.defaults.headers.common['X-CSRF-Token'] = csrfToken;

    InertiaProgress.init({ color: '#4B5563' });


    createInertiaApp({
        resolve: (name) => import(`./components/pages/${name}.tsx`),
        setup({ el, App, props }: {
            el: HTMLElement,
            App: React.ComponentType<{ page: any }>,
            props: any
        }) {
            createRoot(el).render(
                <MantineProvider defaultColorScheme="dark" theme={themeRed}>
                    <App {...props} />
                </MantineProvider>
            );
        },
    });

});
