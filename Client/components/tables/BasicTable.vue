<template>
    <div class="single_sidebar_widget post_category_widget">
        <h4 class="widget_title">Simple Table</h4>
        <ul class="list cat-list">
            <BasicTableElement />
            <BasicTableElement />
            <BasicTableElement />
            <BasicTableElement />
            <BasicTableElement />
            <BasicTableElement />
            <BasicTableElement />
        </ul>
        <div class="br"></div>
        <nuxt/>
    </div>
</template>

<script>
import BasicTableElement from '@/components/tables/BasicTableElement.vue'

export default {
    components: {
        BasicTableElement,
    }
}
</script>

<style>

</style>
