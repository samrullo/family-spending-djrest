# How to pass hostname to react app rom django

Here's the typical process when dealing with React and Django:

1. **Build Phase for React**: During the React app's build phase (when you run something like `npm run build`), any references to environment variables like `process.env.REACT_APP_API_DEV_HOSTNAME` get replaced with their actual values that are set at the time of building. This means that the resulting static files will have these hardcoded values.

2. **Serving with Django**: When you serve these built static files via Django, they're just static assets like any other (like images or CSS). Django isn't processing these files on each request; it's merely serving them as they are. 

If you need your React app to know about certain variables from Django at runtime (i.e., after the React app is built and when it's being used by end-users), you have a couple of common approaches:

1. **Inject into HTML Template**: Have Django render an initial HTML template that includes the variables you need, embedded as global JavaScript variables. Then, your React app can reference these global variables.

    For example, in your Django template:

    ```html
    <script>
        window.REACT_APP_API_HOSTNAME = "{{ api_hostname_from_django }}";
    </script>
    ```

    And in your React code:

    ```javascript
    const API_HOSTNAME = window.REACT_APP_API_HOSTNAME;
    ```

2. **API Endpoint**: Create a simple API endpoint in Django that returns configuration or environment-specific data. Your React app can then make an initial request to this endpoint to get any information it needs.

3. **Django Settings**: If you're building your React app as part of a Django deployment process (e.g., in a Django Docker container), you can access Django settings in your build scripts and feed them to your React app's build process.

Remember, whichever method you choose, always be cautious about which variables you expose to the client side. Never expose sensitive information like secrets or keys.