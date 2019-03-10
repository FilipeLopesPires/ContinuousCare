<template>
    <header class="header">
        <ul class="nav-items">
            <li>
                <nuxt-link to="/">Home</nuxt-link>
            </li>
            <li>
                <nuxt-link to="/history">History</nuxt-link>
            </li>
            <li>
                <nuxt-link to="/devices">Devices</nuxt-link>
            </li>
            <li>
                <nuxt-link to="/about">About</nuxt-link>
            </li>
            <li>
                <nuxt-link to="/settings">Settings</nuxt-link>
            </li>
        </ul>
    </header>
</template>

<style scoped>
    .header {
        width: 100%;
        height: 60px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .nav-items {
        list-style: none;
        padding: 0;
        margin: 0;
        display: flex;
        justify-content: space-around;
        align-items: center;
        width: 100%;
        background-color:royalblue;
    }
</style>
