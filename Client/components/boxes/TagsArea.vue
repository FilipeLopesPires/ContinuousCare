<template>
    <div class="blog_right_sidebar">
        <div class="tag_cloud_widget">
            <div class="row justify-content-center d-flex align-items-center">
                <div class="col-lg-12 col-md-12" v-for="area in availableTags" :key="area.title">
                    <h4 class="widget_title"> {{ area.title }} </h4>
                    <ul>
                        <li class="list" v-for="tag in area.tags" :key="tag.id">
                            <div @click="clickTag(area.title,tag)">
                                <nuxt-link to="" > {{ tag }} </nuxt-link>
                            </div>
                        </li>
                    </ul>
                </div>
                <div class="col-lg-12 col-md-12" v-if="selectedTags.length > 0">
                    <h4 class="widget_title"> Selected </h4>
                    <ul>
                        <li class="list" v-for="selected in selectedTags" :key="selected.tag">
                            <div @click="unclickTag(selected)">
                                <nuxt-link to="" > {{ selected.tag }} </nuxt-link>
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
        var availableTags = []; // [ {title:'', tags:[]}, {...}, ... ]
        var selectedTags = [];  // [ {area:'', tag:''}, {...}, ... ]

        for(var i in this.areas) {
            availableTags.push(this.areas[i]);
        }

        return {
            availableTags,
            selectedTags,
            firstClick: true,
        }
    },
    methods: {
        clickTag(area,tag) {
            // advise user
            if(this.selectedTags.length == 0 && this.firstClick) {
                this.$toasted.show('Remember that once you switch to another page, your selections will be submitted.', 
                    {position: 'bottom-center', duration: 5000});
                this.firstClick = false;
            }
            // add to selected tags
            this.selectedTags.push({area:area, tag:tag});
            // remove from available tags
            for(var a in this.availableTags) {
                if(this.availableTags[a].title == area) {
                    var new_availableTags_tags = [];
                    for(var i in this.availableTags[a].tags) {
                        if(this.availableTags[a].tags[i] != tag) {
                            new_availableTags_tags.push(this.availableTags[a].tags[i]);
                        }
                    }
                    this.availableTags[a].tags = new_availableTags_tags;
                }
            }
        },
        unclickTag(selected) {
            // remove from selected tags
            var new_selectedTags = [];
            for(var i in this.selectedTags) {
                if(this.selectedTags[i].tag != selected.tag) {
                    new_selectedTags.push(this.selectedTags[i]);
                }
            }
            this.selectedTags = new_selectedTags;
            // add to available tags
            for(var i in this.availableTags) {
                if(this.availableTags[i].title == selected.area) {
                    var new_availableTags_tags = [];
                    for(var j in this.availableTags[i].tags) {
                        new_availableTags_tags.push(this.availableTags[i].tags[j]);
                    }
                    new_availableTags_tags.push(selected.tag);
                    this.availableTags[i].tags = new_availableTags_tags;
                }
            }
        }
    }
}
</script>

<style>

</style>
