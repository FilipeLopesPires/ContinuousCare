<template>
    <nav class="blog-pagination justify-content-center d-flex">
        <ul class="pagination">
            <li class="page-item">
                <a href="#" class="page-link" aria-label="Previous">
                    <span aria-hidden="true">
                        <span class="lnr lnr-chevron-left"></span>
                    </span>
                </a>
            </li>
            <li class="page-item active">
                <a href="#" class="page-link">01</a>
            </li>
            <li class="page-item">
                <a href="#" class="page-link">02</a>
            </li>
            <li class="page-item">
                <a href="#" class="page-link">03</a>
            </li>
            <li class="page-item">
                <a href="#" class="page-link">04</a>
            </li>
            <li class="page-item">
                <a href="#" class="page-link">09</a>
            </li>
            <li class="page-item">
                <a href="#" class="page-link" aria-label="Next">
                    <span aria-hidden="true">
                        <span class="lnr lnr-chevron-right"></span>
                    </span>
                </a>
            </li>
        </ul>
    </nav>
</template>

<script>
export default {
    name: 'PaginationBox',
    props: {
        
    }
}
</script>

<style>

</style>
