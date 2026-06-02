mod simple;

fn quick_sort(arr: &mut [i32]) {
    if arr.len() <= 1 {
        return;
    }
    let pivot_index = partition(arr);
    let (left, right) = arr.split_at_mut(pivot_index);
    quick_sort(left);
    quick_sort(&mut right[1..]);
}

fn partition(arr: &mut [i32]) -> usize {
    let len = arr.len();
    let pivot = arr[len - 1];
    let mut i = 0;
    for j in 0..len - 1 {
        if arr[j] <= pivot {
            arr.swap(i, j);
            i += 1;
        }
    }
    arr.swap(i, len - 1);
    i
}

fn quick_sort_interact() {
    let mut arr = [3, 6, 8, 10, 1, 2, 1];
    println!("Before: {:?}", arr);
    quick_sort(&mut arr);
    println!("After: {:?}", arr);
}

fn main() {
    simple::run_simple();
    quick_sort_interact();
}
