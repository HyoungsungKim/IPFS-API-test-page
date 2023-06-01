/** @type {import('next').NextConfig} */
const nextConfig = {}

module.exports = {
    async headers() {
      return [
        {
          source: '/api/:path*', // Specify the API route path or a wildcard pattern
          headers: [
            {
              key: 'Access-Control-Allow-Origin',
              value: '*', // Set the appropriate origin(s) or '*' for all origins
            },
            // Add other CORS headers if needed
          ],
        },
      ];
    },
  };
