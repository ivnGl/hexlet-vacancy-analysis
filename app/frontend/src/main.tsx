import { InertiaProgress } from '@inertiajs/progress';
import { createInertiaApp } from "@inertiajs/react";
import { MantineProvider } from '@mantine/core';
import '@mantine/core/styles.css';
import axios from 'axios';
import { createRoot } from "react-dom/client";

document.addEventListener('DOMContentLoaded', () => {
    const csrfMeta = document.querySelector('meta[name=csrf-token]');
    const csrfToken = csrfMeta ? csrfMeta.getAttribute('content') : '';
    axios.defaults.headers.common['X-CSRF-Token'] = csrfToken;

    InertiaProgress.init({ color: '#4B5563' });

    createInertiaApp({
        resolve: (name) => import(`./components/pages/${name}.tsx`),
        setup({ el, App, props }) {
            createRoot(el).render(
                <MantineProvider defaultColorScheme='dark'><App {...props} /></MantineProvider>
            );
        },
    });
});
