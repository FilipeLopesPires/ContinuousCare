<template>
    <div class="blog_right_sidebar">
        <div class="tag_cloud_widget" v-for="area in areas" 
        :key="area.id">
            <h4 class="widget_title"> {{ area.area.title }} </h4>
            <div class="row justify-content-center d-flex align-items-center">
                <div class="col-lg-9 col-md-9 ">
                    <ul>
                        <li class="list" v-for="tag in area.area.tags"
                        :key="tag.id"><a href="#"> {{ tag }} </a></li>
                    </ul>
                </div>
            </div>
        </div>
        
    </div>
</template>

<script>
export default {
    name: 'TagsArea',
    props: {
        areas: {
            type: Array,
            required: true,
        }
    }
}
</script>

<style>

</style>
