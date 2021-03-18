<template>
    <head>
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=yes">
        <link rel="icon" href="img/logo/logo.png" type="image/png">
        <title>Continuous Care - {{ page }}</title>
    </head>
</template>

<script>
export default {
    name: 'HeaderHTML',
    props: {
        page: {
            type: String,
            required: true
        }
    }
}
</script>

<style>

</style>
