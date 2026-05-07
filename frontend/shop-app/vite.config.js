import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';
import mkcert from 'vite-plugin-mkcert';

export default defineConfig({
	plugins: [mkcert(), sveltekit()],
	test: {
		include: ['src/**/*.{test,spec}.{js,ts}']
	},
	server: {
		fs: {
			// Allow serving files from one level up to the project root
			allow: ['..'],
		  },
		port: 3000,
		host: true,
		https: false,
		proxy: {
			'/api': {
			  target: 'http://shop-api.lensim.de:8080',
			  changeOrigin: true,
			  rewrite: (path) => path.replace(/^\/api/, ''),
			},
		  },
	},
	preview: {
		port: 3000,
		host: true,
		https: false,
	},
	optimizeDeps: {
        include: ['@tensorflow/tfjs', '@tensorflow-models/posenet'],
    },
    ssr: {
        noExternal: ['@tensorflow/tfjs', '@tensorflow-models/posenet'],
    },
});
