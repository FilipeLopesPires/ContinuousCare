<template>
    <div class="blog_right_sidebar">
        <div class="tag_cloud_widget">
            <div class="row justify-content-center d-flex align-items-center">
                <input v-model='new_emotion' @keyup.enter="clickTag(null,new_emotion)" class='single-input mb-20 ml-15 mr-15' placeholder='Type anything you find relevant...'>
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
                    <div class="row justify-content-center d-flex align-items-center">
                        <div class="mt-10 col-lg-8 col-md-9"> </div>
                        <div class="mt-10 col-lg-4 col-md-3 justify-content-center d-flex align-items-center">
                            <button class="genric-btn info radius text-uppercase mb-60" type="button" @click="sendSelected">Done</button>
                        </div>
                    </div>
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
        var new_emotion = null;

        var availableTags = []; // [ {title:'', tags:[]}, {...}, ... ]
        var selectedTags = [];  // [ {area:'', tag:''}, {...}, ... ]

        for(var i in this.areas) {
            availableTags.push(this.areas[i]);
        }

        return {
            new_emotion,
            availableTags,
            selectedTags,
            firstClick: true,
        }
    },
    methods: {
        clickTag(area,tag) {
            // advise user
            /* if(this.selectedTags.length == 0 && this.firstClick) {
                this.$toasted.show('Remember that once you switch to another page, your selections will be submitted.', 
                    {position: 'bottom-center', duration: 5000});
                this.firstClick = false;
            } */
            if(area) {
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
            } else {
                // check if input already exists
                var exists = false;
                for(var i=0; i<this.selectedTags.length; i++) {
                    if(this.selectedTags[i].tag == tag) {
                        exists = true;
                    }
                }
                if(!exists) {
                    // add to selected tags
                    this.selectedTags.push({area:null, tag:tag});
                } else {
                    // toast, warn that no repeated words are allowed
                }
            }
        },
        unclickTag(selected) {
            // remove from selected tags
            var new_selectedTags = [];
            var null_area = false;
            for(var i in this.selectedTags) {
                if(this.selectedTags[i].tag != selected.tag) {
                    new_selectedTags.push(this.selectedTags[i]);
                } else if(this.selectedTags[i].area == null) {
                    null_area = true;
                }
            }
            this.selectedTags = new_selectedTags;
            if(!null_area) {
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
        },
        async sendSelected() {
            // prepare message
            var selection = [];
            for(var i in this.selectedTags) {
                selection.push(this.selectedTags[i].tag);
            }
            var data = {
                'moods': selection,
            }
            const config = {
                headers: {'AuthToken': this.$store.getters.sessionToken},
            }
            // send data
            await this.$axios.$post("/mood", data, config)
                .then(res => {
                    if(res.status != 0) {
                        console.log(res);
                        if(res.status == 4) {
                            this.$toasted.show(res.msg, {position: 'bottom-center', duration: 7500});
                            this.$disconnect()
                            this.$nextTick(() => { 
                                this.$store.dispatch('logout'),
                                this.$router.push("/login")
                            });
                        }
                        this.$toasted.show('Something went wrong while sending your health update. Please try again, if it still does not work, contact us through email.', 
                            {position: 'bottom-center', duration: 7500});
                    } else {
                        this.$toasted.show('Daily update submitted.', 
                            {position: 'bottom-center', duration: 2500});
                        if(process.client) {
                            //window.location.reload(true);
                            var copy = this.$data.selectedTags
                            for(let sel in copy){
                                this.unclickTag(copy[sel])
                            }
                            this.$emit("submited", event)
                        }
                        /*
                        this.availableTags = [];
                        this.selectedTags = [];
                        for(var i in this.areas) {
                            this.availableTags.push(this.areas[i]);
                        }
                        */
                    }
                })
                .catch(e => {
                    console.log(e);
                    this.$toasted.show('Something went wrong while sending your health update. The server might be down at the moment. Please try again later.', 
                        {position: 'bottom-center', duration: 7500});
                });
        },
    }
}
</script>

<style>

</style>
