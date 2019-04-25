<template>
    <div class="blog_right_sidebar">
        <div class="tag_cloud_widget" v-for="area in areas" :key="area.id">
            <h4 class="widget_title"> {{ area.area.title }} </h4>
            <div class="row justify-content-center d-flex align-items-center">
                <div class="col-lg-9 col-md-9 ">
                    <ul>
                        <li class="list" v-for="tag in area.area.tags" :key="tag.id">
                            <div @click="clickTag(area.area,tag)">
                                <nuxt-link to="" > {{ tag }} </nuxt-link>
                            </div>
                        </li>
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
    },
    data() {
        var selectedAreas = []
        for(var area in Object.keys(this.areas)) {
            selectedAreas.push({
                title: area.title,
                tags: [],
            })
        }
        return {
            selectedAreas,
        }
    },
    methods: {
        isSelected(area,tag) {
            return false
        },
        clickTag(area,tag) {
            console.log(area)
            console.log(tag)
            console.log(this.selectedAreas)
        }
    }
}
</script>

<style>

</style>
